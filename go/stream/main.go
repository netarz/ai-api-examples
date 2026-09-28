// Streaming chat completion (Server-Sent Events), standard library only.
//
// Each event is a line "data: {...}" and the stream ends with "data: [DONE]".
// The last chunk before [DONE] carries `usage`; the gateway adds it for every
// provider, so stream_options.include_usage is not needed.
//
// Run:
//
//	export NETARZ_API_KEY="sk-ntz-v1-..."
//	go run ./stream
//
// Docs: https://netarz.ir/docs/ai/streaming
package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

type message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type chatRequest struct {
	Model     string    `json:"model"`
	Messages  []message `json:"messages"`
	MaxTokens int       `json:"max_tokens"`
	Stream    bool      `json:"stream"`
}

type chunk struct {
	Choices []struct {
		Delta struct {
			Content string `json:"content"`
		} `json:"delta"`
	} `json:"choices"`
	Usage *struct {
		TotalTokens int `json:"total_tokens"`
	} `json:"usage"`
}

func env(name, fallback string) string {
	if v := os.Getenv(name); v != "" {
		return v
	}
	return fallback
}

func main() {
	key := os.Getenv("NETARZ_API_KEY")
	if key == "" {
		fmt.Fprintln(os.Stderr, "Set NETARZ_API_KEY first")
		os.Exit(1)
	}
	baseURL := env("NETARZ_BASE_URL", "https://netarz.ir/api/ai/v1")

	body, err := json.Marshal(chatRequest{
		Model:     env("NETARZ_MODEL", "gpt-4o-mini"),
		Messages:  []message{{Role: "user", Content: "یک شعر کوتاه دربارهٔ پاییز بنویسید."}},
		MaxTokens: 200,
		Stream:    true,
	})
	if err != nil {
		panic(err)
	}

	req, err := http.NewRequest(http.MethodPost, baseURL+"/chat/completions", bytes.NewReader(body))
	if err != nil {
		panic(err)
	}
	req.Header.Set("Authorization", "Bearer "+key)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "text/event-stream")

	// A long answer from a reasoning model can take minutes; keep the timeout generous.
	client := &http.Client{Timeout: 5 * time.Minute}
	res, err := client.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stderr, "request failed:", err)
		os.Exit(1)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		// Errors before the first token come back as a normal JSON body.
		raw, _ := io.ReadAll(res.Body)
		fmt.Fprintf(os.Stderr, "HTTP %d: %s\n", res.StatusCode, raw)
		os.Exit(1)
	}

	scanner := bufio.NewScanner(res.Body)
	scanner.Buffer(make([]byte, 0, 64*1024), 1024*1024)
	for scanner.Scan() {
		line := scanner.Text()
		if !strings.HasPrefix(line, "data:") {
			continue // blank separators and ": keep-alive" comments
		}
		data := strings.TrimSpace(strings.TrimPrefix(line, "data:"))
		if data == "[DONE]" {
			break
		}

		var c chunk
		if err := json.Unmarshal([]byte(data), &c); err != nil {
			continue
		}
		if len(c.Choices) > 0 {
			fmt.Print(c.Choices[0].Delta.Content)
		}
		if c.Usage != nil {
			fmt.Printf("\n\ntokens: %d\n", c.Usage.TotalTokens)
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "\nstream interrupted:", err)
		os.Exit(1)
	}
}
