"""
Agent CLI 
Typer를 사용한 에이전트 대화 인터페이스
"""

import asyncio
from typing import List, Dict
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.panel import Panel
from pydantic import ValidationError

from .default import DefaultAgent
from .settings import get_settings

app = typer.Typer(help="Agent Lab CLI - 에이전트와 대화하기")
console = Console()
settings = get_settings()


@app.command()
def chat(
    model: str = typer.Option(None, "--model", "-m", help="사용할 OpenAI 모델 (기본값: 설정에서 로드)"),
    system_prompt: str = typer.Option(None, "--system", "-s", help="시스템 프롬프트"),
):
    """기본 에이전트와 대화를 시작합니다."""
    
    # 설정 유효성 검사
    try:
        # 설정 로드 시도 (ValidationError 발생 가능)
        api_key = settings.openai_api_key
        used_model = model or settings.openai_model
    except ValidationError as e:
        console.print(f"[red]설정 오류: {e}[/red]")
        console.print("OPENAI_API_KEY 환경변수가 설정되지 않았거나 잘못되었습니다.")
        console.print("다음과 같이 설정해주세요:")
        console.print("export OPENAI_API_KEY='your-api-key-here'")
        raise typer.Exit(1)
    
    console.print(Panel.fit(
        f"[bold blue]Agent Lab Chat[/bold blue]\n"
        f"모델: {used_model}\n"
        f"온도: {settings.openai_temperature}\n"
        f"종료: /quit, /exit 또는 Ctrl+C",
        border_style="blue"
    ))
    
    # 에이전트 초기화
    try:
        agent = DefaultAgent(model_name=model)
    except Exception as e:
        console.print(f"[red]에이전트 초기화 실패: {e}[/red]")
        raise typer.Exit(1)
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
                    response = asyncio.run(agent.invoke_legacy(user_input, chat_history[:-1]))
                    
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
    try:
        # 현재 설정값 표시
        console.print(Panel(
            f"[bold blue]Agent Lab CLI[/bold blue]\n\n"
            f"현재 설정:\n"
            f"• 모델: {settings.openai_model}\n"
            f"• 온도: {settings.openai_temperature}\n"
            f"• 타임아웃: {settings.agent_timeout}초\n"
            f"• 최대 재시도: {settings.agent_max_retries}회\n\n"
            f"사용 가능한 명령어:\n"
            f"• [cyan]chat[/cyan] - 기본 에이전트와 대화\n"
            f"• [cyan]info[/cyan] - 이 정보 표시\n\n"
            f"환경변수 설정:\n"
            f"• [yellow]OPENAI_API_KEY[/yellow] - OpenAI API 키 (필수)\n"
            f"• [yellow]OPENAI_MODEL[/yellow] - 기본 모델명\n"
            f"• [yellow]OPENAI_TEMPERATURE[/yellow] - 모델 온도 (0.0-2.0)\n"
            f"• [yellow]AGENT_TIMEOUT[/yellow] - 응답 타임아웃 (초)",
            border_style="green"
        ))
    except ValidationError as e:
        console.print(f"[red]설정 로드 실패: {e}[/red]")
        console.print("필수 환경변수가 설정되지 않았습니다.")
        console.print("OPENAI_API_KEY를 설정해주세요.")


if __name__ == "__main__":
    app()
