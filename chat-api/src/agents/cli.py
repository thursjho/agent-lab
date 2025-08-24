"""
Agent CLI 
Typer를 사용한 에이전트 대화 인터페이스
"""

import asyncio
import os
from typing import List, Dict
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.panel import Panel

from .default import DefaultAgent

app = typer.Typer(help="Agent Lab CLI - 에이전트와 대화하기")
console = Console()


@app.command()
def chat(
    model: str = typer.Option("gpt-4o-mini", "--model", "-m", help="사용할 OpenAI 모델"),
    system_prompt: str = typer.Option(None, "--system", "-s", help="시스템 프롬프트"),
):
    """기본 에이전트와 대화를 시작합니다."""
    
    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY 환경변수가 설정되지 않았습니다.[/red]")
        console.print("다음과 같이 설정해주세요:")
        console.print("export OPENAI_API_KEY='your-api-key-here'")
        raise typer.Exit(1)
    
    console.print(Panel.fit(
        f"[bold blue]Agent Lab Chat[/bold blue]\n"
        f"모델: {model}\n"
        f"종료: /quit, /exit 또는 Ctrl+C",
        border_style="blue"
    ))
    
    # 에이전트 초기화
    agent = DefaultAgent(model_name=model)
    chat_history: List[Dict[str, str]] = []
    
    # 시스템 프롬프트 추가
    if system_prompt:
        chat_history.append({"role": "system", "content": system_prompt})
        console.print(f"[dim]시스템 프롬프트 설정: {system_prompt}[/dim]")
    
    try:
        while True:
            # 사용자 입력
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            # 종료 명령어 확인
            if user_input.lower() in ["/quit", "/exit", "quit", "exit"]:
                console.print("[yellow]대화를 종료합니다.[/yellow]")
                break
            
            if not user_input.strip():
                continue
            
            # 채팅 기록에 사용자 메시지 추가
            chat_history.append({"role": "user", "content": user_input})
            
            # 에이전트 응답 생성
            with console.status("[bold green]생각 중...[/bold green]"):
                try:
                    response = asyncio.run(agent.invoke(user_input, chat_history[:-1]))
                    
                    # 응답 출력
                    console.print("\n[bold green]Assistant[/bold green]")
                    console.print(Markdown(response))
                    
                    # 채팅 기록에 응답 추가
                    chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    console.print(f"[red]오류가 발생했습니다: {e}[/red]")
                    # 실패한 경우 사용자 메시지를 히스토리에서 제거
                    chat_history.pop()
    
    except KeyboardInterrupt:
        console.print("\n[yellow]대화를 종료합니다.[/yellow]")
    except Exception as e:
        console.print(f"[red]예상치 못한 오류: {e}[/red]")


@app.command()
def info():
    """에이전트 정보를 출력합니다."""
    console.print(Panel(
        "[bold blue]Agent Lab CLI[/bold blue]\n\n"
        "사용 가능한 명령어:\n"
        "• [cyan]chat[/cyan] - 기본 에이전트와 대화\n"
        "• [cyan]info[/cyan] - 이 정보 표시\n\n"
        "환경변수 설정:\n"
        "• [yellow]OPENAI_API_KEY[/yellow] - OpenAI API 키 (필수)",
        border_style="green"
    ))


if __name__ == "__main__":
    app()
