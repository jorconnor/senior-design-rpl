package gin

import (
	"fmt"
	"io"
	"os"
	"time"

	"github.com/mattn/go-isatty"
)

var (
	green   = string([]byte{27, 91, 57, 55, 59, 52, 50, 109})
	white   = string([]byte{27, 91, 57, 48, 59, 52, 55, 109})
	yellow  = string([]byte{27, 91, 57, 55, 59, 52, 51, 109})
	red     = string([]byte{27, 91, 57, 55, 59, 52, 49, 109})
	blue    = string([]byte{27, 91, 57, 55, 59, 52, 52, 109})
	magenta = string([]byte{27, 91, 57, 55, 59, 52, 53, 109})
	cyan    = string([]byte{27, 91, 57, 55, 59, 52, 54, 109})
	reset   = string([]byte{27, 91, 48, 109})
)

func ErrorLogger() HandlerFunc {
	return ErrorLoggerT(ErrorTypeAny)
}

func ErrorLoggerT(typ ErrorType) HandlerFunc {
	return func(c *Context) {
		c.Next()
		errors := c.Errors.ByType(typ)
		if len(errors) > 0 {
			c.JSON(-1, errors)
		}
	}
}

func Logger() HandlerFunc {
	return LoggerWithWriter(DefaultWriter)
}

func LoggerWithWriter(out io.Writer, notlogged ...string) HandlerFunc {
	isTerm := true

	if w, ok := out.(*os.File); !ok || !isatty.IsTerminal(w.Fd()) {
		isTerm = false
	}

	var skip map[string]struct{}

	if length := len(notlogged); length > 0 {
		skip = make(map[string]struct{}, length)

		for _, path := range notlogged {
			skip[path] = struct{}{}
		}
	}

	return func(c *Context) {
		start := time.Now()
		path := c.Request.URL.Path


		c.Next()

		if _, ok := skip[path]; !ok {
			end := time.Now()
			latency := end.Sub(start)

			clientIP := c.ClientIP()
			method := c.Request.Method
			statusCode := c.Writer.Status()
			var statusColor, methodColor string
			if isTerm {
				statusColor = colorForStatus(statusCode)
				methodColor = colorForMethod(method)
			}
			comment := c.Errors.ByType(ErrorTypePrivate).String()

			fmt.Fprintf(out, "[GIN] %v |%s %3d %s| %13v | %s |%s  %s %-7s %s\n%s",
				end.Format("2006/01/02 - 15:04:05"),
				statusColor, statusCode, reset,
				latency,
				clientIP,
				methodColor, reset, method,
				path,
				comment,
			)
		}
	}
}

func colorForStatus(code int) string {
	switch {
	case code >= 200 && code < 300:
		return green
	case code >= 300 && code < 400:
		return white
	case code >= 400 && code < 500:
		return yellow
	default:
		return red
	}
}

func colorForMethod(method string) string {
	switch method {
	case "GET":
		return blue
	case "POST":
		return cyan
	case "PUT":
		return yellow
	case "DELETE":
		return red
	case "PATCH":
		return green
	case "HEAD":
		return magenta
	case "OPTIONS":
		return white
	default:
		return reset
	}
}