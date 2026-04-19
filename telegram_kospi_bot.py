import telepot
import FinanceDataReader as fdr
from datetime import datetime
import os

# GitHub Secrets에서 설정한 환경 변수를 불러옵니다.
# 로컬에서 테스트할 때는 직접 문자열을 넣어도 되지만, GitHub 업로드 시에는 이대로 유지하세요.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_kospi_report():
    """
    KOSPI 지수 데이터를 가져와 분석 메시지를 생성합니다.
    """
    try:
        # 코스피(KS11) 데이터 호출
        df = fdr.DataReader('KS11')
        
        # 마지막 2일치 데이터 추출 (종가 기준)
        current_data = df.iloc[-1]
        prev_data = df.iloc[-2]
        
        current_price = current_data['Close']
        change = current_price - prev_data['Close']
        change_percent = (change / prev_data['Close']) * 100
        
        # 등락 상태 심볼 및 텍스트 설정
        if change > 0:
            symbol = "📈 상승"
        elif change < 0:
            symbol = "📉 하락"
        else:
            symbol = "⚖️ 보합"

        # 현재 시간 포맷팅
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 텔레그램으로 보낼 메시지 구성
        message = (
            f"🔔 [주간 코스피 리포트]\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📅 시간: {now}\n"
            f"📍 지수: {current_price:,.2f}\n"
            f"📊 변동: {change:+.2f} ({change_percent:+.2f}%)\n"
            f"📢 상태: {symbol}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"오늘도 성공적인 투자 되세요! 💪"
        )
        return message
    except Exception as e:
        return f"❌ 데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"

def send_telegram_msg(text):
    """
    텔레그램 메시지를 전송합니다.
    """
    # 환경 변수 설정 확인
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("설정 에러: TELEGRAM_TOKEN 또는 CHAT_ID 환경 변수가 없습니다.")
        return

    try:
        # 텔레그램 봇 객체 생성 및 메시지 전송
        bot = telepot.Bot(TELEGRAM_TOKEN)
        bot.sendMessage(CHAT_ID, text)
        print("✅ 텔레그램 메시지 전송 완료!")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

if __name__ == "__main__":
    # 리포트 생성 및 전송 실행
    content = get_kospi_report()
    send_telegram_msg(content)
