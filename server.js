const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'ui')));

app.post('/api/register_asset', (req, res) => {
    const { name, value, owner } = req.body;
    let category = "أصل عام / غير مصنف";
    const lowerName = name.toLowerCase();
    
    if (lowerName.includes('أرض') || lowerName.includes('عقار') || lowerName.includes('منزل') || lowerName.includes('بناء')) {
        category = "أصل عقاري (Real Estate)";
    } else if (lowerName.includes('عملة') || lowerName.includes('رمز') || lowerName.includes('تشفير') || lowerName.includes('nft')) {
        category = "أصل رقمي (Digital Asset)";
    } else if (lowerName.includes('خدمة') || lowerName.includes('برمجة') || lowerName.includes('استشارة') || lowerName.includes('عمل')) {
        category = "أصل خدمي (Service)";
    }

    const referenceId = "ASSET-" + Math.random().toString(36).substr(2, 9).toUpperCase();
    res.json({ message: "Success", category, referenceId });
});

app.post('/api/ai_chat', (req, res) => {
    const { message, username } = req.body;
    const referenceId = "GOV-" + Math.random().toString(36).substr(2, 9).toUpperCase();
    const response = `[نظام التوثيق الذكي] مرحباً ${username}. تم توثيق طلبك (Ref: ${referenceId}) المتعلق بـ "${message}" في دفتر الأستاذ الرقمي لـ Omniverse Hub.`;
    res.json({ message: response });
});

app.listen(PORT, () => console.log(`Omniverse Hub Engine Active`));