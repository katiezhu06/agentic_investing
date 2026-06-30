# Agentic Investing

Connect [Cursor](https://cursor.com) to Robinhood Agentic Trading via the Model Context Protocol (MCP), so your agent can read portfolio data and place trades in a dedicated Agentic account.

## Prerequisites

- A Robinhood individual investing account in good standing
- Access to [Robinhood Agentic Trading](https://robinhood.com/us/en/support/articles/agentic-trading-overview/) (rolling out gradually)
- [Cursor](https://cursor.com) with MCP support
- A desktop browser for OAuth and Agentic account setup

## Setup

This repo includes a project-level MCP config at [`.cursor/mcp.json`](.cursor/mcp.json):

```json
{
  "mcpServers": {
    "robinhood-trading": {
      "url": "https://agent.robinhood.com/mcp/trading"
    }
  }
}
```

1. Clone this repo and open it in Cursor.
2. Restart Cursor (or reload the window) so it loads the MCP server.
3. Open **Cursor Settings** (`Cmd + Shift + J` on Mac, `Ctrl + Shift + J` on Windows/Linux).
4. Go to **Tools & MCPs** and confirm `robinhood-trading` is listed.
5. Complete Robinhood OAuth when prompted, then open and fund your Agentic account if you have not already.

### Alternative: global config

To use Robinhood MCP in every project, add the same entry to `~/.cursor/mcp.json` instead.

## Usage

Use **Agent** mode in Cursor and ask in natural language, for example:

- "Show my Robinhood portfolio and buying power."
- "Get a quote for AAPL."
- "Review a market order for 1 share of MSFT before placing it."

Cursor will request approval before each MCP tool call. Review every action carefully before approving.

Trades are placed only in your **Robinhood Agentic account**, not your primary investing account.

## Troubleshooting

- **Server not appearing:** Restart Cursor and check **Output → MCP Logs** (`Cmd + Shift + U`).
- **Auth issues:** Disconnect and reconnect the server in **Tools & MCPs**, or remove and re-add the entry in `mcp.json`.
- **Onboarding:** Agentic account setup must be completed on desktop. If you started on mobile, open the onboarding URL in a desktop browser.

## References

- [Robinhood Agentic Trading overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)
- [Cursor MCP documentation](https://cursor.com/docs/mcp)

## Disclaimer

Agentic trading involves significant risk, including possible loss of your entire investment. You are responsible for trades your AI agent places. Robinhood does not supervise connected agents. Review Robinhood's disclosures before using this setup.
