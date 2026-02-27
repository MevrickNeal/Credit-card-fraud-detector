<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Payment Gateway</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: { fontFamily: { sans: ['Inter', 'sans-serif'] }, colors: { brand: '#0f172a', brand_hover: '#1e293b' } }
            }
        }
    </script>
    <style>
        .fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        input[type="number"]::-webkit-inner-spin-button, input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 font-sans min-h-screen flex items-center justify-center p-4">

    <!-- Main Card Container -->
    <div class="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] w-full max-w-md overflow-hidden border border-gray-100">
        <div class="px-8 pt-8 pb-6 border-b border-gray-100">
            <div class="flex items-center justify-between mb-2">
                <h1 class="text-xl font-bold text-gray-900">Checkout</h1>
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <p class="text-sm text-gray-500">Enter your payment details below.</p>
        </div>

        <div class="p-8">
            <div class="space-y-5">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Payment Amount</label>
                    <div class="relative">
                        <span class="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">$</span>
                        <input type="number" id="amount" value="50.00" class="w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand focus:border-brand outline-none transition-all font-medium text-gray-900" oninput="updateButton()">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Card Number</label>
                    <div class="relative">
                        <input type="text" id="cardNumber" placeholder="0000 0000 0000 0000" class="w-full pl-4 pr-10 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand focus:border-brand outline-none transition-all font-mono text-sm tracking-wider">
                        <svg class="absolute right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
                    </div>
                </div>
                <div class="flex gap-4">
                    <div class="w-1/2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">Expiry Date</label>
                        <input type="text" id="expiry" placeholder="MM/YY" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand focus:border-brand outline-none transition-all text-center">
                    </div>
                    <div class="w-1/2">
                        <label class="block text-sm font-medium text-gray-700 mb-1">CVV</label>
                        <input type="text" id="cvv" placeholder="123" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand focus:border-brand outline-none transition-all text-center">
                    </div>
                </div>
                <button id="payBtn" onclick="processPayment()" class="w-full mt-2 bg-brand hover:bg-brand_hover text-white font-semibold py-4 rounded-xl shadow-lg shadow-brand/20 transition-all flex justify-center items-center gap-2 group">
                    <span id="btnText">Pay $50.00</span>
                    <svg id="btnIcon" class="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                    <svg id="btnSpinner" class="hidden animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                </button>
            </div>
        </div>

        <div id="resultBanner" class="hidden px-8 py-5 border-t border-gray-100 fade-in">
            <div id="resultContent" class="flex items-start gap-3">
                <div id="resultIcon"></div>
                <div>
                    <h3 id="resultTitle" class="font-bold text-gray-900"></h3>
                    <p id="resultDesc" class="text-sm text-gray-600 mt-1"></p>
                    <div class="mt-2 flex items-center gap-2 text-xs font-mono bg-gray-50 px-2 py-1 rounded inline-block border border-gray-100">
                        <span id="resultRisk" class="font-semibold"></span> | Latency: <span id="resultLatency" class="text-gray-500"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Sandbox Mode Floating Panel -->
    <div class="fixed bottom-6 right-6 w-80 bg-white rounded-2xl shadow-2xl border border-gray-100 z-50 overflow-hidden transition-all duration-300">
        <button onclick="toggleSandbox()" class="w-full flex items-center justify-between p-5 hover:bg-gray-50 transition-colors focus:outline-none">
            <div class="flex items-center gap-3">
                <span class="flex h-2 w-2 relative"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span></span>
                <h4 class="text-xs font-bold tracking-wider text-indigo-600 uppercase">Sandbox Environment</h4>
            </div>
            <svg id="sandboxChevron" class="w-5 h-5 text-gray-400 transform transition-transform duration-300 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg>
        </button>
        
        <div id="sandboxContent" class="px-5 pb-5 hidden">
            <p class="text-xs text-gray-500 mb-3">Generate random valid test profiles.</p>
            <div class="space-y-2">
                <button onclick="fillRandomProfile('normal')" class="w-full flex items-center justify-between p-3 rounded-xl border border-gray-100 hover:border-green-200 hover:bg-green-50 transition-colors group text-left">
                    <div class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-green-500"></div><span class="text-sm font-medium text-gray-800">Random Normal (4000)</span></div>
                    <svg class="w-4 h-4 text-gray-400 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                </button>
                <button onclick="fillRandomProfile('fraud')" class="w-full flex items-center justify-between p-3 rounded-xl border border-gray-100 hover:border-red-200 hover:bg-red-50 transition-colors group text-left">
                    <div class="flex items-center gap-2"><div class="w-2 h-2 rounded-full bg-red-500"></div><span class="text-sm font-medium text-gray-800">Random Fraud (5000)</span></div>
                    <svg class="w-4 h-4 text-gray-400 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
                </button>
            </div>
        </div>
    </div>

    <script>
        function updateButton() {
            const amount = document.getElementById('amount').value;
            document.getElementById('btnText').innerText = amount ? `Pay $${amount}` : 'Pay Now';
        }

        function toggleSandbox() {
            document.getElementById('sandboxContent').classList.toggle('hidden');
            document.getElementById('sandboxChevron').classList.toggle('rotate-180');
        }

        // SMART LUHN GENERATOR: Generates cards that pass Layer 1 Math Check
        function generateValidLuhnCard(prefix) {
            let card = prefix;
            // Generate up to 15 digits
            while (card.length < 15) {
                card += Math.floor(Math.random() * 10).toString();
            }
            // Calculate what the 16th check digit should be
            let sum = 0;
            let alternate = true;
            for (let i = card.length - 1; i >= 0; i--) {
                let n = parseInt(card.charAt(i));
                if (alternate) {
                    n *= 2;
                    if (n > 9) n -= 9;
                }
                sum += n;
                alternate = !alternate;
            }
            let checkDigit = (10 - (sum % 10)) % 10;
            let finalCard = card + checkDigit;
            
            // Format nicely with spaces
            return finalCard.substring(0,4) + ' ' + finalCard.substring(4,8) + ' ' + finalCard.substring(8,12) + ' ' + finalCard.substring(12,16);
        }

        function fillRandomProfile(type) {
            let card = '';
            if (type === 'normal') card = generateValidLuhnCard('4000');
            else if (type === 'fraud') card = generateValidLuhnCard('5000');

            const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0');
            const year = String(Math.floor(Math.random() * 5) + 24); 
            const cvv = Math.floor(Math.random() * 900 + 100).toString();

            document.getElementById('cardNumber').value = card;
            document.getElementById('expiry').value = `${month}/${year}`;
            document.getElementById('cvv').value = cvv;
            
            ['cardNumber', 'expiry', 'cvv'].forEach(id => {
                const el = document.getElementById(id);
                el.classList.add('ring-2', 'ring-indigo-400', 'bg-indigo-50');
                setTimeout(() => el.classList.remove('ring-2', 'ring-indigo-400', 'bg-indigo-50'), 300);
            });
        }

        async function processPayment() {
            const btn = document.getElementById('payBtn');
            const resultBanner = document.getElementById('resultBanner');
            btn.disabled = true;
            document.getElementById('btnText').innerText = "Analyzing...";
            document.getElementById('btnIcon').classList.add('hidden');
            document.getElementById('btnSpinner').classList.remove('hidden');
            btn.classList.add('opacity-80', 'cursor-not-allowed');
            resultBanner.classList.add('hidden');

            const payload = {
                card_number: document.getElementById('cardNumber').value.replace(/\s/g, ''),
                amount: parseFloat(document.getElementById('amount').value || 0),
                cvv: document.getElementById('cvv').value,
                expiry: document.getElementById('expiry').value
            };

            const startTime = performance.now();

            try {
                const response = await fetch('http://127.0.0.1:8000/process_payment', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                const actualLatency = Math.round(performance.now() - startTime) + 'ms';
                const resultIcon = document.getElementById('resultIcon');
                
                if (response.ok && data.status === "APPROVED") {
                    resultBanner.className = "px-8 py-5 border-t border-green-100 bg-green-50/50 fade-in block";
                    resultIcon.innerHTML = `<div class="p-2 bg-green-100 rounded-full text-green-600"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg></div>`;
                    document.getElementById('resultTitle').innerText = "Payment Successful";
                    document.getElementById('resultTitle').className = "font-bold text-green-800";
                    document.getElementById('resultRisk').className = "font-semibold text-green-600";
                } else {
                    resultBanner.className = "px-8 py-5 border-t border-red-100 bg-red-50/50 fade-in block";
                    resultIcon.innerHTML = `<div class="p-2 bg-red-100 rounded-full text-red-600"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></div>`;
                    document.getElementById('resultTitle').innerText = "Transaction Declined";
                    document.getElementById('resultTitle').className = "font-bold text-red-800";
                    document.getElementById('resultRisk').className = "font-semibold text-red-600";
                }

                document.getElementById('resultDesc').innerText = data.reason || data.detail;
                if(data.risk_score !== undefined) {
                    document.getElementById('resultRisk').innerText = `Risk Score: ${(data.risk_score * 100).toFixed(2)}%`;
                    document.getElementById('resultLatency').innerText = actualLatency;
                } else {
                    document.getElementById('resultRisk').innerText = `System Error/Validation`;
                    document.getElementById('resultLatency').innerText = actualLatency;
                }

            } catch (error) {
                resultBanner.className = "px-8 py-5 border-t border-orange-100 bg-orange-50/50 fade-in block";
                document.getElementById('resultIcon').innerHTML = `<div class="p-2 bg-orange-100 rounded-full text-orange-600"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg></div>`;
                document.getElementById('resultTitle').innerText = "Connection Failed";
                document.getElementById('resultTitle').className = "font-bold text-orange-800";
                document.getElementById('resultDesc').innerText = "Could not connect to the ML backend. Ensure FastAPI is running on 127.0.0.1:8000.";
                document.getElementById('resultRisk').innerText = "API Offline";
                document.getElementById('resultLatency').innerText = "-";
            } finally {
                btn.disabled = false;
                updateButton(); 
                document.getElementById('btnIcon').classList.remove('hidden');
                document.getElementById('btnSpinner').classList.add('hidden');
                btn.classList.remove('opacity-80', 'cursor-not-allowed');
            }
        }
    </script>
</body>
</html>
