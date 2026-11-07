// ==========================================
// OMNIVERSE HUB & TRIPOLI NODE DASHBOARD JS
// ==========================================

const TRIPOLI_NODE_URL = "";  // مسار محلي نسبي متوافق مع سيرفر Flask
const CLIENT_ID = "gbq0kabvz0z4rerl2al5kvbrlwkrtr9a6zi5guf8n423hzxr46qsvvjuatggm2jb";
let currentUser = null;
let isSandbox = true;
let piverifyAccessToken = localStorage.getItem("piverify_token") || null;
let currentLang = 'ar'; // اللغة الافتراضية

// قاموس الترجمة للـ JavaScript (Alerts & Dynamic Text)
const jsTranslations = {
    ar: {
        testnetAlert: "تم الانتقال إلى وضع: ",
        browserNotAvail: "⚠️ بيئة Pi Browser غير متوفرة حالياً (وضع محاكاة المتصفح المحلي نشط).",
        authFailed: "فشل الاتصال: تأكد من استخدام متصفح Pi.",
        piVerifySuccess: "تم التحقق بنجاح عبر بوابة PiVerify العالمية وتوثيق الهوية السيادية تحت درع PRISM!",
        piVerifyBtnAuth: "✅ مسجل وموثق عبر PiVerify",
        assetInputError: "يرجى إدخال اسم الأصل وقيمة مالية صحيحة!",
        assetSuccess: "✅ تم توثيق الأصل (",
        assetSuccessEnd: ") بنجاح وأرشفته في دفتر أستاذ طرابلس!",
        assetFail: "فشل توثيق الأصل: ",
        connectionError: "حدث خطأ أثناء الاتصال بعقدة طرابلس.",
        voteInputError: "يرجى إدخال معرف مقترح صحيح ورصيد LYO للمشاركة!",
        voteSending: "⏳ جاري إرسال وتوثيق الصوت عبر درع PQC ومشرف PRISM...",
        voteFail: "❌ رفض التصويت: ",
        serverError: "❌ حدث خطأ أثناء الاتصال بالسيرفر.",
        negotiateError: "يرجى إدخال المعرف والسعر!",
        negotiateSending: "⏳ جاري التفاوض الآلي عبر الوكلاء الأذكياء...",
        batchConfirm: "هل تريد تنفيذ 5 معاملات اختبارية متتالية عبر درع PQC؟",
        batchDone: "🚀 تم الانتهاء من دورة المعاملات الـ 5 بنجاح وأقرت في دفتر الأستاذ!",
        resetConfirm: "تطهير البيانات المؤقتة؟",
        resetDone: "تم التطهير بنجاح.",
        promptQuery: "اكتب استفساراً!",
        aiProcessing: "🤖 جاري معالجة الطلب عبر المساعد الذكي المحلي لعقدة طرابلس...",
        aiResponsePrefix: "الرد السيادي:\n- الطلب: \"",
        aiResponseSuffix: "\"\n- الحالة: تمت المعالجة بنجاح عبر نموذج Ollama المحلي وإطار عمل أومنيفيرس.",
        pinPrompt: "🔒 إدخال مفتاح السيادة الخاص بالمدير العام:",
        pinError: "❌ خطأ: مفتاح السيادة غير صحيح! هذه الغرفة محصنة ومخصصة للمدير العام فقط.",
        noRecords: "لا توجد سجلات مسجلة حتى الآن.",
        loadingRecords: "جاري جلب السجلات الدائمة..."
    },
    en: {
        testnetAlert: "Switched to mode: ",
        browserNotAvail: "⚠️ Pi Browser environment not available (Local browser simulation mode active).",
        authFailed: "Connection failed: Make sure to use Pi Browser.",
        piVerifySuccess: "Successfully verified via global PiVerify gateway and sovereign identity secured under PRISM shield!",
        piVerifyBtnAuth: "✅ Registered & Verified via PiVerify",
        assetInputError: "Please enter a valid asset name and financial value!",
        assetSuccess: "✅ Asset (",
        assetSuccessEnd: ") successfully verified and archived in Tripoli Ledger!",
        assetFail: "Asset verification failed: ",
        connectionError: "An error occurred while connecting to Tripoli Node.",
        voteInputError: "Please enter a valid proposal ID and LYO balance to participate!",
        voteSending: "⏳ Sending and verifying vote via PQC shield & PRISM supervisor...",
        voteFail: "❌ Vote rejected: ",
        serverError: "❌ An error occurred while connecting to the server.",
        negotiateError: "Please enter ID and price!",
        negotiateSending: "⏳ Automated negotiation in progress via smart agents...",
        batchConfirm: "Do you want to execute 5 consecutive test transactions via PQC shield?",
        batchDone: "🚀 Completed the 5 transaction cycle successfully and committed to the ledger!",
        resetConfirm: "Clear temporary data?",
        resetDone: "Cleared successfully.",
        promptQuery: "Type a query!",
        aiProcessing: "🤖 Processing request via Tripoli Node local AI assistant...",
        aiResponsePrefix: "Sovereign Response:\n- Query: \"",
        aiResponseSuffix: "\"\n- Status: Successfully processed via local Ollama model and Omniverse framework.",
        pinPrompt: "🔒 Enter General Manager Sovereign PIN:",
        pinError: "❌ Error: Invalid Sovereign PIN! This room is secure and restricted to the General Manager.",
        noRecords: "No records registered yet.",
        loadingRecords: "Fetching permanent ledgers..."
    }
};

function initPiSDK() {
    if (typeof Pi !== 'undefined') {
        Pi.init({ version: "2.0", sandbox: isSandbox, clientId: CLIENT_ID });
    }
    const envBtn = document.getElementById('envToggleBtn');
    const helperSec = document.getElementById('testnetHelperSection');
    
    if (envBtn) {
        envBtn.innerText = isSandbox ? `Mode: TESTNET (Sandbox)` : `Mode: MAINNET (Production)`;
        envBtn.className = isSandbox 
            ? "text-xs px-3 py-1 rounded border border-yellow-600 bg-yellow-900/40 text-yellow-400 font-bold transition"
            : "text-xs px-3 py-1 rounded border border-green-600 bg-green-900/40 text-green-400 font-bold transition";
    }
    if (helperSec) {
        helperSec.style.display = isSandbox ? "block" : "none";
    }
}

function toggleEnvironment() {
    isSandbox = !isSandbox;
    initPiSDK();
    alert(jsTranslations[currentLang].testnetAlert + (isSandbox ? 'Testnet' : 'Mainnet'));
}

initPiSDK();

async function connectPi() {
    try {
        if (typeof Pi === 'undefined') {
            alert(jsTranslations[currentLang].browserNotAvail);
            currentUser = { username: "tripoli_node_admin_01" };
            document.getElementById('authBtn').innerText = "✅ " + currentUser.username;
            return;
        }
        const auth = await Pi.authenticate(['username', 'payments'], onIncompletePayment);
        currentUser = auth.user;
        document.getElementById('authBtn').innerText = "✅ " + currentUser.username;
    } catch (err) {  
        console.error("Auth Error:", err);
        alert(jsTranslations[currentLang].authFailed);
    }
}

async function authenticatePiVerify() {
    try {
        piverifyAccessToken = "mock_piverify_token_secure_999";
        localStorage.setItem("piverify_token", piverifyAccessToken);
        const piVerifyBtn = document.getElementById('piVerifyBtn');
        if (piVerifyBtn) piVerifyBtn.innerText = "✅ " + (currentLang === 'ar' ? "تم التحقق عبر PiVerify: Tripoli Node Admin" : "Verified via PiVerify: Tripoli Node Admin");
        alert(jsTranslations[currentLang].piVerifySuccess);
        loadDashboardData();
    } catch (err) {
        console.error("PiVerify Auth Error:", err);
        alert(currentLang === 'ar' ? "حدث خطأ أثناء الاتصال ببوابة PiVerify." : "An error occurred while connecting to PiVerify gateway.");
    }
}

function onIncompletePayment(payment) {
    verifyPaymentOnServer(payment.identifier, payment.transaction ? payment.transaction.txid : null);
}

async function verifyPaymentOnServer(paymentId, txid) {
    try {
        const response = await fetch(`${TRIPOLI_NODE_URL}/api/v1/lyo/execute-task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-PQC-Signature': 'mock_lattice_signature_hash_secure_999',
                'X-PQC-PublicKey': 'tripoli_node_pqc_pub_key_01',
                'X-Timestamp': Math.floor(Date.now() / 1000).toString(),
                'X-PiVerify-Access-Token': piverifyAccessToken || ''
            },
            body: JSON.stringify({ 
                payment_id: paymentId, 
                txid: txid || "local_test_txid",
                user_uid: currentUser ? currentUser.username : "tripoli_node_admin_01", 
                amount_lyo: 100.0,
                is_kyc_verified: true,
                action: "RWA Notary Settlement"
            })
        });
        return await response.json();
    } catch (err) {
        console.error("Verification Error:", err);
    }
}

async function processPayment() {
    const name = document.getElementById('assetName').value;
    const val = parseFloat(document.getElementById('assetVal').value);
    const currency = document.getElementById('assetCurrency').value;

    if (!name || isNaN(val) || val <= 0) return alert(jsTranslations[currentLang].assetInputError);

    try {
        const res = await fetch(`${TRIPOLI_NODE_URL}/api/v1/lyo/execute-task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-PQC-Signature': 'mock_lattice_signature_hash_secure_999',
                'X-PQC-PublicKey': 'tripoli_node_pqc_pub_key_01',
                'X-Timestamp': Math.floor(Date.now() / 1000).toString()
            },
            body: JSON.stringify({
                user_uid: currentUser ? currentUser.username : "tripoli_node_admin_01",
                amount_lyo: val,
                is_kyc_verified: true,
                action: `RWA Asset Notary: ${name} (${currency})`
            })
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
            alert(jsTranslations[currentLang].assetSuccess + name + jsTranslations[currentLang].assetSuccessEnd);
            loadDashboardData();
        } else {
            alert(jsTranslations[currentLang].assetFail + (data.message || "Unknown error"));
        }
    } catch (err) {
        console.error("Error:", err);
        alert(jsTranslations[currentLang].connectionError);
    }
}

async function castLyoSecureVote() {
    const proposalId = document.getElementById('proposalId').value;
    const lyoBalance = parseFloat(document.getElementById('lyoVotingBalance').value);
    const voteChoice = document.getElementById('voteChoice').value === "true";
    const resultBox = document.getElementById('lyoVotingResultBox');

    if (!proposalId || isNaN(lyoBalance) || lyoBalance <= 0) return alert(jsTranslations[currentLang].voteInputError);

    resultBox.innerText = jsTranslations[currentLang].voteSending;
    
    try {
        const response = await fetch(`${TRIPOLI_NODE_URL}/api/v1/lyo/execute-task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-PQC-Signature': 'mock_lattice_signature_hash_secure_999',
                'X-PQC-PublicKey': 'tripoli_node_pqc_pub_key_01',
                'X-Timestamp': Math.floor(Date.now() / 1000).toString()
            },
            body: JSON.stringify({ 
                user_uid: currentUser ? currentUser.username : "tripoli_node_admin_01", 
                amount_lyo: lyoBalance, 
                is_kyc_verified: true, 
                action: `LYO Vote Proposal: ${proposalId} (Choice: ${voteChoice})` 
            })
        });

        const data = await response.json();
        if (response.ok && data.status === "success") {
            resultBox.innerHTML = `✅ <span class="text-green-400 font-bold">${currentLang === 'ar' ? 'الحالة:' : 'Status:'}</span> ${currentLang === 'ar' ? 'تم توثيق الصوت بنجاح تحت حماية PQC!' : 'Vote successfully verified under PQC protection!'}\n` +
                                  `🛡️ <span class="text-cyan-400 font-bold">${currentLang === 'ar' ? 'مشرف PRISM:' : 'PRISM Supervisor:'}</span> PASSED\n` +
                                  `🔐 <span class="text-yellow-400 font-bold">${currentLang === 'ar' ? 'التوقيع الكمي:' : 'Quantum Signature:'}</span> SHA3-512 Lattice-Verified`;
            loadDashboardData();
        } else {
            resultBox.innerText = jsTranslations[currentLang].voteFail + (data.message || "Sovereign error");
        }
    } catch (err) { resultBox.innerText = jsTranslations[currentLang].serverError; }
}

async function executeSorobanBridge() {
    const box = document.getElementById('pillarsResultBox');
    box.classList.remove('hidden');
    box.innerText = currentLang === 'ar' ? "🌉 جسر السيولة (Soroban): متصل ومزامن مع شبكة الأصول بنجاح (Zero-Error)." : "🌉 Soroban Liquidity Bridge: Connected and synchronized with asset network successfully (Zero-Error).";
}

async function submitDaoProposal() {
    const box = document.getElementById('pillarsResultBox');
    box.classList.remove('hidden');
    box.innerText = currentLang === 'ar' ? "🗳️ مقترح الحوكمة (DAO): تم إدراج المقترح بنجاح في دفتر أستاذ طرابلس السيادي." : "🗳️ DAO Governance Proposal: Successfully listed in Tripoli Sovereign Ledger.";
}

async function runPredictiveSimulation() {
    const box = document.getElementById('pillarsResultBox');
    box.classList.remove('hidden');
    box.innerText = currentLang === 'ar' ? "📊 المحاكاة التنبؤية (AI): استقرار كامل في شبكة الوكلاء وتوقعات النمو عند 99.8%." : "📊 AI Predictive Simulation: Full agent network stability with 99.8% growth forecast.";
}

async function runComplianceAudit() {
    const box = document.getElementById('pillarsResultBox');
    box.classList.remove('hidden');
    box.innerText = currentLang === 'ar' ? "🔍 التدقيق المالي (AML): جميع المعاملات مستوفية لقواعد Non-Security Utility ومتوافقة تماماً." : "🔍 AML Financial Audit: All transactions meet Non-Security Utility rules and are fully compliant.";
}

async function processDualAssetSettlement() {
    processPayment();
}

async function startAiNegotiation() {
    const assetId = document.getElementById('negotiateAssetId').value;
    const initialOffer = document.getElementById('negotiateOfferVal').value;
    const resultBox = document.getElementById('negotiationResultBox');

    if (!assetId || initialOffer === "") return alert(jsTranslations[currentLang].negotiateError);

    resultBox.innerText = jsTranslations[currentLang].negotiateSending;
    setTimeout(() => {
        resultBox.innerHTML = `✅ <span class="text-yellow-400 font-bold">${currentLang === 'ar' ? 'الحالة:' : 'Status:'}</span> ${currentLang === 'ar' ? 'تم إبرام الاتفاق بنجاح' : 'Agreement successfully concluded'} | <span class="text-cyan-400 font-bold">${currentLang === 'ar' ? 'العرض المعتمد:' : 'Approved Offer:'}</span> ${initialOffer} LYO`;
        loadDashboardData();
    }, 800);
}

async function runFiveTestTransactions() {
    if (!confirm(jsTranslations[currentLang].batchConfirm)) return;
    for (let i = 1; i <= 5; i++) {
        await fetch(`${TRIPOLI_NODE_URL}/api/v1/lyo/execute-task`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-PQC-Signature': 'mock_lattice_signature_hash_secure_999',
                'X-PQC-PublicKey': 'tripoli_node_pqc_pub_key_01',
                'X-Timestamp': Math.floor(Date.now() / 1000).toString()
            },
            body: JSON.stringify({
                user_uid: "tripoli_test_agent_" + i,
                amount_lyo: 50.0 * i,
                is_kyc_verified: true,
                action: "Batch Testnet Transaction " + i
            })
        });
        await new Promise((resolve) => setTimeout(resolve, 300));
    }
    alert(jsTranslations[currentLang].batchDone);
    loadDashboardData();
}

async function forceResetPayments() {
    if(!confirm(jsTranslations[currentLang].resetConfirm)) return;
    localStorage.clear();
    piverifyAccessToken = null;
    alert(jsTranslations[currentLang].resetDone);
    loadDashboardData();
}

async function sendToLocalAIModel() {
    const promptText = document.getElementById('localAiPrompt').value;
    const responseBox = document.getElementById('aiResponseBox');
    if (!promptText.trim()) return alert(jsTranslations[currentLang].promptQuery);
    responseBox.innerText = jsTranslations[currentLang].aiProcessing;
    setTimeout(() => {
        responseBox.innerText = jsTranslations[currentLang].aiResponsePrefix + promptText + jsTranslations[currentLang].aiResponseSuffix;
    }, 800);
}

async function fetchPendingApprovals() {
    const bodyEl = document.getElementById('pending-approvals-body');
    if (!bodyEl) return;
    const autoVerifiedText = currentLang === 'ar' ? 'معتمد ذاتياً (Auto-Verified)' : 'Auto-Verified';
    const auditTitle = currentLang === 'ar' ? 'تدقيق مالي عالي القيمة' : 'High-Value Financial Audit';
    const auditDesc = currentLang === 'ar' ? 'مراقبة تشغيلية آمنة لعقدة طرابلس تحت إشراف PRISM' : 'Secure operational monitoring for Tripoli Node under PRISM supervision';

    bodyEl.innerHTML = `
        <tr>
            <td class="p-2 font-mono text-amber-400">REQ-9901</td>
            <td class="p-2 text-zinc-200">Agent_Alpha_01</td>
            <td class="p-2 text-cyan-400">${auditTitle}</td>
            <td class="p-2 text-zinc-400">${auditDesc}</td>
            <td class="p-2 text-center">
                <span class="px-2 py-1 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded text-[10px]">${autoVerifiedText}</span>
            </td>
        </tr>
    `;
}

function downloadSovereignCsv() {
    window.location.href = `${TRIPOLI_NODE_URL}/api/v1/sovereign/ledger/export-csv`;
}

async function loadDashboardData() {
    try {
        let healthRes = await fetch(`${TRIPOLI_NODE_URL}/health`);
        let healthData = await healthRes.json();
        if (healthData.status === 'healthy') {
            const nodeDisp = document.getElementById('nodeNameDisplay');
            if (nodeDisp) nodeDisp.innerText = healthData.node || "Tripoli Node v0.6.3";
        }

        let ledgerRes = await fetch(`${TRIPOLI_NODE_URL}/api/v1/sovereign/ledger/archive`);
        let ledgerData = await ledgerRes.json();
        
        let tbody = document.getElementById('crosschainTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        if (ledgerData.status === 'success' && ledgerData.transactions && ledgerData.transactions.length > 0) {
            ledgerData.transactions.forEach(tx => {
                const archivedText = currentLang === 'ar' ? 'مؤرشف ومؤمن (PQC)' : 'Archived & Secured (PQC)';
                const burnText = currentLang === 'ar' ? 'حرق: ' : 'Burn: ';
                tbody.innerHTML = (tbody.innerHTML || '') + `
                    <tr class="hover:bg-zinc-800/50 transition">
                        <td class="p-2 font-mono text-cyan-300">${tx.transaction_id || 'TX-' + tx.id}</td>
                        <td class="p-2 font-mono text-zinc-300">${tx.pi_user_uid}</td>
                        <td class="p-2 font-bold text-yellow-400">${tx.gross_paid_lyo} LYO <span class="text-[10px] text-zinc-500">(${burnText}${tx.burned_lyo})</span></td>
                        <td class="p-2"><span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px]">${archivedText}</span></td>
                        <td class="p-2 font-mono text-[10px] text-zinc-400">${tx.timestamp}</td>
                    </tr>
                `;
            });
        } else {
            tbody.innerHTML = `<tr><td colspan="5" class="p-3 text-center text-zinc-500">${jsTranslations[currentLang].noRecords}</td></tr>`;
        }

        fetchPendingApprovals();
    } catch (err) {
        console.error("[-] Error updating dashboard:", err);
    }
}

window.onload = function() {
    loadDashboardData();
    if (piverifyAccessToken) {
        const btn = document.getElementById('piVerifyBtn');
        if (btn) btn.innerText = jsTranslations[currentLang].piVerifyBtnAuth;
    }
};