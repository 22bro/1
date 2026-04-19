import telepot
import FinanceDataReader as fdr
from datetime import datetime
import os

# GitHub Secrets에서 설정한 환경 변수를 안전하게 가져옵니다.
# 주의: 로컬 테스트가 아닌 GitHub Actions 실행용입니다.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_kospi_report():
    """
    KOSPI 지수 데이터를 분석하여 메시지를 생성합니다.
    """
    try:
        # 코스피(KS11) 데이터 호출
        df = fdr.DataReader('KS11')
        
        # 마지막 2거래일 데이터 추출
        current_data = df.iloc[-1]
        prev_data = df.iloc[-2]
        
        current_price = current_data['Close']
        change = current_price - prev_data['Close']
        change_percent = (change / prev_data['Close']) * 100
        
        # 등락 심볼 설정
        if change > 0:
            symbol = "📈 상승"
        elif change < 0:
            symbol = "📉 하락"
        else:
            symbol = "⚖️ 보합"

        # 현재 시간 포맷
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 메시지 구성 (가독성을 위한 이모지 및 구분선 활용)
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
        return f"❌ 데이터 분석 중 오류가 발생했습니다: {str(e)}"

def send_telegram_msg(text):
    """
    텔레그램 봇을 통해 메시지를 전송합니다.
    """
    # 환경 변수 설정 여부 체크
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("설정 오류: TELEGRAM_TOKEN 또는 CHAT_ID 환경 변수를 찾을 수 없습니다.")
        return

    try:
        # 텔레그램 봇 객체 생성 및 메시지 전송
        bot = telepot.Bot(TELEGRAM_TOKEN)
        bot.sendMessage(CHAT_ID, text)
        print("✅ 텔레그램 메시지 전송에 성공했습니다.")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")

if __name__ == "__main__":
    # 리포트 생성 및 전송 실행
    content = get_kospi_report()
    send_telegram_msg(content)
