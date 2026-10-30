# app.py
from flask import Flask, render_template_string

app = Flask(__name__)

# Serve the HTML you provided (as a template string).
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Loan Application - Steps</title>
  <style>
    :root{
      --bg:#f3f4f6;
      --card:#ffffff;
      --text:#111827;
      --muted:#6b7280;
      --line:#e5e7eb;
      --primary:#f59e0b; /* orange */
      --primary-dark:#d97706;
      --shadow: 0 10px 30px rgba(0,0,0,.08);
      --radius:14px;
      --field-radius:8px;
    }

    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
      background: var(--bg);
      color: var(--text);
      display:flex;
      justify-content:center;
      min-height:100vh;
    }

    .app-shell{
      width: 420px;
      padding: 18px 14px 40px;
    }

    /* Header bars (to mimic screenshots) */
    .topbar{
      height: 44px;
      border-radius: 12px;
      background: #111827;
      margin-bottom: 16px;
      position: relative;
      overflow: hidden;
      display:flex;
      align-items:center;
      padding: 0 14px;
      color:#fff;
      font-weight:600;
      letter-spacing:.2px;
      opacity:.95;
    }
    .topbar .title{
      margin-left: auto;
      font-size: 13px;
      opacity:.9;
    }

    .screen{
      background: transparent;
      display:none;
    }
    .screen.active{display:block;}

    .card{
      background: var(--card);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 22px 18px;
      margin-top: 10px;
    }

    /* Welcome screen */
    .welcome-title{
      text-align:center;
      font-weight:800;
      font-size: 18px;
      margin: 2px 0 6px;
    }
    .welcome-sub{
      text-align:center;
      color:var(--muted);
      font-size: 12px;
      margin: 0 0 14px;
      line-height:1.3;
    }

    .calc-wrap{
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 14px 12px;
      background: #fafafa;
    }
    .calc-row{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:10px;
      margin-bottom: 10px;
    }
    .calc-left{
      flex:1;
    }
    .calc-label{
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
      font-weight: 600;
    }
    .calc-value{
      font-size: 14px;
      font-weight: 800;
      color: #111827;
    }
    .calc-pill{
      background:#fff;
      border:1px solid var(--line);
      padding:10px 12px;
      border-radius: 12px;
      width: 150px;
      text-align:center;
      background: #fff;
    }
    .calc-pill .big{
      font-size: 18px;
      font-weight:900;
      color: #111827;
    }
    .calc-pill .small{
      margin-top:4px;
      font-size: 12px;
      color: var(--muted);
    }

    .range-area{
      margin-top: 10px;
      display:flex;
      flex-direction:column;
      gap: 8px;
    }
    .range-row{
      display:flex;
      justify-content:space-between;
      font-size: 12px;
      color: var(--muted);
    }
    input[type="range"]{
      width:100%;
      accent-color: var(--primary);
    }

    .cta{
      width:100%;
      margin-top: 14px;
      border: none;
      border-radius: 10px;
      background: var(--primary);
      color:#111827;
      padding: 12px 14px;
      font-weight: 900;
      cursor:pointer;
    }
    .cta:active{transform: translateY(1px);}

    /* Loan application card */
    .step-title{
      text-align:center;
      font-weight: 900;
      margin: 0;
      font-size: 16px;
    }
    .progress-bar{
      margin: 10px 0 14px;
      height: 6px;
      background: #f3f4f6;
      border-radius: 999px;
      overflow:hidden;
    }
    .progress-bar > span{
      display:block;
      height:100%;
      width: 0%;
      background: var(--primary);
    }

    .fields{
      display:flex;
      flex-direction:column;
      gap: 14px;
      margin-top: 6px;
    }

    .field-label{
      font-size: 12px;
      color: var(--muted);
      font-weight: 700;
      margin-bottom: 6px;
    }

    .two-col{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .control{
      width: 100%;
      border: 1px solid var(--line);
      background: #fff;
      border-radius: var(--field-radius);
      padding: 11px 12px;
      font-size: 13px;
      outline:none;
    }
    .control:focus{
      border-color: #fbbf24;
      box-shadow: 0 0 0 4px rgba(245,158,11,.2);
    }

    .textarea{
      min-height: 70px;
      resize: none;
    }

    .summary{
      border: 1px solid var(--line);
      border-left: 4px solid var(--primary);
      border-radius: 10px;
      padding: 12px;
      background: #fff;
    }
    .summary .summary-title{
      font-weight: 900;
      font-size: 12px;
      margin-bottom: 8px;
      color: #111827;
    }
    .summary-grid{
      display:grid;
      grid-template-columns: 92px 1fr;
      row-gap: 6px;
      column-gap: 10px;
      font-size: 12px;
    }
    .summary-grid .k{
      color: var(--muted);
      font-weight: 700;
    }
    .summary-grid .v{
      font-weight: 900;
      color:#111827;
    }

    .actions{
      display:flex;
      gap: 12px;
      margin-top: 16px;
    }
    .btn{
      flex:1;
      border:none;
      border-radius: 10px;
      padding: 11px 12px;
      font-weight: 900;
      cursor:pointer;
      font-size: 13px;
    }
    .btn.secondary{
      background: #e5e7eb;
      color:#111827;
    }
    .btn.primary{
      background: var(--primary);
      color:#111827;
    }
    .btn:active{transform: translateY(1px);}

    /* Minor helper */
    .muted{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
    }

    /* Make it look like a phone viewport spacing */
    .spacer-top{height: 6px;}
  </style>
</head>

<body>
  <div class="app-shell">
    <div class="topbar">
      <div>◀</div>
      <div class="title">OneMoney</div>
    </div>

    <!-- SCREEN 1: Welcome -->
    <section class="screen active" id="screen-1" aria-label="Welcome">
      <div class="card">
        <h2 class="welcome-title">Welcome to OneMoney</h2>
        <p class="welcome-sub">
          Fast & easy loans — Get Money in Minutes
        </p>

        <div class="calc-wrap" role="group" aria-label="Loan Calculator">
          <div class="calc-row">
            <div class="calc-left">
              <div class="calc-label">Loan Calculator</div>

              <div style="display:flex; gap:14px; margin-top:2px; align-items:flex-end;">
                <div>
                  <div class="calc-label" style="margin-bottom:4px;">Amount</div>
                  <div class="calc-value">ZWL 55,000</div>
                </div>
                <div>
                  <div class="calc-label" style="margin-bottom:4px;">Duration</div>
                  <div class="calc-value">12 Months</div>
                </div>
              </div>
            </div>

            <div class="calc-pill">
              <div class="big">ZWL 4,584</div>
              <div class="small">Monthly Payment</div>
            </div>
          </div>

          <div class="range-area">
            <input type="range" min="20000" max="100000" value="55000" />
            <div class="range-row">
              <span>ZWL 20,000</span>
              <span>ZWL 100,000</span>
            </div>
          </div>

          <button class="cta" type="button">GET STARTED</button>
        </div>
      </div>
    </section>

    <!-- SCREEN 2: Step 1 -->
    <section class="screen" id="screen-2" aria-label="Loan Application Step 1">
      <div class="card">
        <h2 class="step-title">Loan Application</h2>

        <div class="progress-bar" aria-hidden="true">
          <span style="width: 25%"></span>
        </div>

        <div class="muted" style="text-align:center; font-weight:800; margin-top:-6px;">
          Step 1 of 3
        </div>

        <div class="fields">
          <div>
            <div class="field-label">First Name &amp; Last Name</div>
            <div class="two-col">
              <input class="control" type="text" placeholder="First name" aria-label="First Name" />
              <input class="control" type="text" placeholder="Last name" aria-label="Last Name" />
            </div>
          </div>

          <div>
            <div class="field-label">Phone Number (Zimbabwe)</div>
            <input class="control" type="tel" placeholder="+263 712345678" aria-label="Phone Number" />
            <div class="muted" style="margin-top:6px;">
              +263 digits only, e.g. 0712345678
            </div>
          </div>

          <div class="actions">
            <button class="btn secondary" type="button">BACK</button>
            <button class="btn primary" type="button">NEXT</button>
          </div>
        </div>
      </div>
    </section>

    <!-- SCREEN 3: Step 2 -->
    <section class="screen" id="screen-3" aria-label="Loan Application Step 2">
      <div class="card">
        <h2 class="step-title">Loan Application</h2>

        <div class="progress-bar" aria-hidden="true">
          <span style="width: 55%"></span>
        </div>

        <div class="muted" style="text-align:center; font-weight:800; margin-top:-6px;">
          Step 1 of 3
        </div>

        <div class="fields">
          <div>
            <div class="field-label">Loan Type</div>
            <select class="control" aria-label="Loan Type">
              <option selected>Business Loan</option>
              <option>Personal Loan</option>
              <option>Education Loan</option>
            </select>
          </div>

          <div>
            <div class="field-label">Amount (ZWL)</div>
            <input class="control" type="text" placeholder="20000" aria-label="Amount" />
          </div>

          <div>
            <div class="field-label">Loan Duration</div>
            <select class="control" aria-label="Loan Duration">
              <option selected>24 Months</option>
              <option>6 Months</option>
              <option>12 Months</option>
              <option>36 Months</option>
            </select>
          </div>

          <div>
            <div class="field-label">Loan Purpose</div>
            <textarea class="control textarea" placeholder="Describe the purpose of your loan..." aria-label="Loan Purpose"></textarea>
          </div>

          <div class="actions">
            <button class="btn primary" type="button" style="flex:1;">NEXT</button>
          </div>
        </div>
      </div>
    </section>

    <!-- SCREEN 4: Step 3 -->
    <section class="screen" id="screen-4" aria-label="Loan Application Step 3">
      <div class="card">
        <h2 class="step-title">Loan Application</h2>

        <div class="progress-bar" aria-hidden="true">
          <span style="width: 85%"></span>
        </div>

        <div class="muted" style="text-align:center; font-weight:800; margin-top:-6px;">
          Step 1 of 3
        </div>

        <div class="fields">
          <div>
            <div class="field-label">Employment Status</div>
            <select class="control" aria-label="Employment Status">
              <option selected>Self-Employed</option>
              <option>Employed</option>
              <option>Unemployed</option>
              <option>Student</option>
            </select>
          </div>

          <div>
            <div class="field-label">Annual Income (ZWL)</div>
            <input class="control" type="text" placeholder="Enter your annual income" aria-label="Annual Income" />
          </div>

          <div class="summary" aria-label="Application Summary">
            <div class="summary-title">Application Summary</div>
            <div class="summary-grid">
              <div class="k">Amount:</div>
              <div class="v">20,000 ZWL</div>

              <div class="k">Duration:</div>
              <div class="v">24 Months</div>

              <div class="k">Purpose:</div>
              <div class="v">—</div>

              <div class="k">Applicant:</div>
              <div class="v">—</div>
            </div>
          </div>

          <div class="actions">
            <button class="btn secondary" type="button">BACK</button>
            <button class="btn primary" type="button">SUBMIT</button>
          </div>
        </div>
      </div>
    </section>
  </div>

  <script>
    // Optional: simple navigation demo (remove if not needed)
    const screens = [
      document.getElementById('screen-1'),
      document.getElementById('screen-2'),
      document.getElementById('screen-3'),
      document.getElementById('screen-4'),
    ];

    function showScreen(i){
      screens.forEach(s => s.classList.remove('active'));
      screens[i].classList.add('active');
    }

    // Welcome -> Step 1
    document.querySelector('#screen-1 .cta')?.addEventListener('click', () => showScreen(1));

    // Step 1 NEXT -> Step 2
    document.querySelector('#screen-2 .btn.primary')?.addEventListener('click', () => showScreen(2));

    // Step 2 NEXT -> Step 3
    document.querySelector('#screen-3 .btn.primary')?.addEventListener('click', () => showScreen(3));

    // Step 2 BACK -> Step 1
    document.querySelector('#screen-2 .btn.secondary')?.addEventListener('click', () => showScreen(1));

    // Step 3 BACK -> Step 2
    document.querySelector('#screen-4 .btn.secondary')?.addEventListener('click', () => showScreen(2));
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # http://127.0.0.1:5000
    app.run(debug=True)

