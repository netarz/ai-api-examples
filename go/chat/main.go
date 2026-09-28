// Basic chat completion through the NetArz AI gateway, standard library only.
//
// Run:
//
//	export NETARZ_API_KEY="sk-ntz-v1-..."
//	go run ./chat
//
// Docs: https://netarz.ir/docs/ai/chat-completions
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
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
}

type chatResponse struct {
	ID      string `json:"id"`
	Choices []struct {
		Message message `json:"message"`
	} `json:"choices"`
	Usage struct {
		PromptTokens     int `json:"prompt_tokens"`
		CompletionTokens int `json:"completion_tokens"`
		TotalTokens      int `json:"total_tokens"`
	} `json:"usage"`
}

// apiError is the OpenAI-shaped error body: {"error": {"message", "type", "code", "param"}}.
type apiError struct {
	Error struct {
		Message string `json:"message"`
		Code    string `json:"code"`
	} `json:"error"`
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
		// Any id from https://netarz.ir/ai-api/models, e.g.
		// "openrouter/anthropic/claude-sonnet-4.5", "gemini-3.5-flash", "deepseek-flash".
		Model: env("NETARZ_MODEL", "gpt-4o-mini"),
		Messages: []message{
			{Role: "system", Content: "شما دستیار فارسی‌زبان یک فروشگاه اینترنتی هستید. کوتاه و دقیق جواب بدهید."},
			{Role: "user", Content: "برای یک فروشگاه لوازم ورزشی یک شعار کوتاه بنویسید."},
		},
		// Always send max_tokens: the gateway reserves credit for the largest
		// possible answer before the call, so a cap keeps that reservation small.
		MaxTokens: 200,
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

	client := &http.Client{Timeout: 120 * time.Second}
	res, err := client.Do(req)
	if err != nil {
		fmt.Fprintln(os.Stderr, "request failed:", err)
		os.Exit(1)
	}
	defer res.Body.Close()

	raw, err := io.ReadAll(res.Body)
	if err != nil {
		panic(err)
	}

	if res.StatusCode != http.StatusOK {
		var e apiError
		_ = json.Unmarshal(raw, &e)
		fmt.Fprintf(os.Stderr, "HTTP %d %s: %s\n", res.StatusCode, e.Error.Code, e.Error.Message)
		os.Exit(1)
	}

	var out chatResponse
	if err := json.Unmarshal(raw, &out); err != nil {
		panic(err)
	}
	if len(out.Choices) == 0 {
		fmt.Fprintln(os.Stderr, "no choices in response")
		os.Exit(1)
	}

	fmt.Println(out.Choices[0].Message.Content)
	// out.ID is the NetArz request id (same as the X-Request-Id header).
	fmt.Printf("\nrequest id: %s | tokens: %d\n", out.ID, out.Usage.TotalTokens)
}
