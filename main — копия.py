import random
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()


# Вспомогательная функция для генерации на Python
def generate_numbers(min_val: int, max_val: int, count: int):
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    count = max(1, min(count, 50))
    numbers = [str(random.randint(min_val, max_val)) for _ in range(count)]
    return ", ".join(numbers), min_val, max_val, count


# 1. Новый маршрут для получения чисел без перезагрузки страницы (для анимации)
@app.get("/api/generate")
def api_generate(min_val: int = 1, max_val: int = 100, count: int = 1):
    result_text, _, _, _ = generate_numbers(min_val, max_val, count)
    return JSONResponse(content={"result": result_text})


# 2. Основная страница
@app.get("/", response_class=HTMLResponse)
def show_number(min_val: int = 1, max_val: int = 100, count: int = 1):
    result_text, min_val, max_val, count = generate_numbers(min_val, max_val, count)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Рандомайзер</title>
        <link rel="preconnect" href="https://googleapis.com">
        <link rel="preconnect" href="https://gstatic.com" crossorigin>
        <link href="https://googleapis.com/css2?family=Nunito:wght@500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                color-scheme: dark;
            }}

            .container {{
                background: #1e293b;
                padding: 32px 28px;
                border-radius: 28px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 0 20px 35px rgba(0, 0, 0, 0.4);
                width: 100%;
                max-width: 340px;
                text-align: center;
            }}

            h2 {{
                font-size: 24px;
                font-weight: 800;
                margin-bottom: 24px;
                color: #f1f5f9;
            }}

            .input-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 14px;
            }}

            label {{
                font-size: 16px;
                font-weight: 600;
                color: #94a3b8;
            }}

            input {{
                padding: 10px 14px;
                width: 110px;
                font-size: 17px;
                font-family: 'Nunito', sans-serif;
                font-weight: 700;
                color: #ffffff;
                background-color: #0f172a;
                border: 2px solid #334155;
                border-radius: 16px;
                text-align: center;
                outline: none;
                transition: border-color 0.2s, box-shadow 0.2s;
            }}

            input:focus {{
                border-color: #38bdf8;
                box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
            }}

            button.main-btn {{
                width: 100%;
                padding: 14px 24px;
                background-color: #0088cc;
                color: white;
                border: none;
                border-radius: 18px;
                cursor: pointer;
                margin-top: 14px;
                font-size: 17px;
                font-family: 'Nunito', sans-serif;
                font-weight: 800;
                box-shadow: 0 4px 15px rgba(0, 136, 204, 0.35);
                transition: background-color 0.2s, transform 0.1s, box-shadow 0.2s, opacity 0.2s;
            }}

            button.main-btn:hover {{
                background-color: #0099e6;
                box-shadow: 0 6px 20px rgba(0, 136, 204, 0.5);
            }}

            button.main-btn:active {{
                transform: scale(0.96);
            }}

            button.main-btn:disabled {{
                opacity: 0.7;
                cursor: not-allowed;
            }}

            .result-window {{
                margin-top: 24px;
                padding: 20px 16px 14px 16px;
                background-color: #162032;
                border: 2px dashed #334155;
                border-radius: 20px;
                min-height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                position: relative;
            }}

            .result-label {{
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                color: #64748b;
                margin-bottom: 6px;
                font-weight: 700;
            }}

            #result {{
                font-size: 34px;
                font-weight: 800;
                color: #38bdf8;
                word-break: break-word;
                transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), color 0.2s;
                margin-bottom: 12px;
            }}

            .rolling {{
                color: #94a3b8 !important;
                transform: scale(0.92);
                filter: blur(0.4px);
            }}

            .pop {{
                transform: scale(1.12);
                text-shadow: 0 0 18px rgba(56, 189, 248, 0.6);
            }}

            /* Стили для кнопки копирования */
            .copy-btn {{
                padding: 6px 14px;
                background-color: transparent;
                border: 2px solid #334155;
                color: #94a3b8;
                border-radius: 12px;
                cursor: pointer;
                font-size: 12px;
                font-weight: 700;
                font-family: 'Nunito', sans-serif;
                text-transform: uppercase;
                transition: all 0.2s;
            }}

            .copy-btn:hover {{
                border-color: #38bdf8;
                color: #38bdf8;
                background-color: rgba(56, 189, 248, 0.1);
            }}

            .copy-btn:active {{
                transform: scale(0.95);
            }}

            .copy-btn.success {{
                border-color: #10b981;
                color: #10b981;
                background-color: rgba(16, 185, 129, 0.1);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Генератор чисел</h2>

            <form id="gen_form">
                <div class="input-row">
                    <label for="min_val">От:</label>
                    <input type="number" id="min_val" name="min_val" value="{min_val}" required>
                </div>

                <div class="input-row">
                    <label for="max_val">До:</label>
                    <input type="number" id="max_val" name="max_val" value="{max_val}" required>
                </div>

                <div class="input-row">
                    <label for="count">Количество:</label>
                    <input type="number" id="count" name="count" value="{count}" min="1" max="50" required>
                </div>

                <button type="submit" id="submit_btn" class="main-btn">Сгенерировать!</button>
            </form>

            <div class="result-window">
                <span class="result-label">Результат</span>
                <div id="result">{result_text}</div>
                <button type="button" id="copy_btn" class="copy-btn">Копировать</button>
            </div>
        </div>

        <script>
            const form = document.getElementById('gen_form');
            const resultDiv = document.getElementById('result');
            const submitBtn = document.getElementById('submit_btn');
            const copyBtn = document.getElementById('copy_btn');

            let audioCtx;

            // Функция для легкого звука "тиканья"
            function playTick() {{
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                if (audioCtx.state === 'suspended') audioCtx.resume();

                const osc = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                osc.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                osc.type = 'sine';
                osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);

                gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.05);

                osc.start();
                osc.stop(audioCtx.currentTime + 0.05);
            }}

            // Функция для звука завершения
            function playDing() {{
                if (!audioCtx) return;
                const osc = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                osc.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                osc.type = 'triangle';
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);

                osc.start();
                osc.stop(audioCtx.currentTime + 0.3);
            }}

            // Логика копирования
            copyBtn.addEventListener('click', () => {{
                navigator.clipboard.writeText(resultDiv.textContent).then(() => {{
                    copyBtn.textContent = 'Скопировано!';
                    copyBtn.classList.add('success');
                    setTimeout(() => {{
                        copyBtn.textContent = 'Копировать';
                        copyBtn.classList.remove('success');
                    }}, 1500);
                }});
            }});

            form.addEventListener('submit', async (e) => {{
                e.preventDefault(); 

                // Инициализируем аудиоконтекст по клику пользователя, если он еще не создан
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();

                let min = parseInt(document.getElementById('min_val').value) || 1;
                let max = parseInt(document.getElementById('max_val').value) || 100;
                let count = parseInt(document.getElementById('count').value) || 1;

                if (min > max) [min, max] = [max, min];
                count = Math.max(1, Math.min(count, 50));

                submitBtn.disabled = true;
                submitBtn.textContent = 'Крутим...';
                resultDiv.classList.remove('pop');
                resultDiv.classList.add('rolling');

                const fetchPromise = fetch(`/api/generate?min_val=${{min}}&max_val=${{max}}&count=${{count}}`)
                    .then(res => res.json());

                // Запускаем крутку случайных чисел и звук тиканья барабана каждые 60 мс
                const interval = setInterval(() => {{
                    playTick();
                    const fakeNums = [];
                    for (let i = 0; i < count; i++) {{
                        fakeNums.push(Math.floor(Math.random() * (max - min + 1)) + min);
                    }}
                    resultDiv.textContent = fakeNums.join(', ');
                }}, 60);

                const [data] = await Promise.all([
                    fetchPromise,
                    new Promise(resolve => setTimeout(resolve, 600))
                ]);

                clearInterval(interval);
                resultDiv.classList.remove('rolling');
                resultDiv.textContent = data.result;

                // Проигрываем финальный звук и эффект прыжка
                playDing();
                resultDiv.classList.add('pop');
                setTimeout(() => resultDiv.classList.remove('pop'), 300);

                submitBtn.disabled = false;
                submitBtn.textContent = 'Сгенерировать!';
            }});
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)