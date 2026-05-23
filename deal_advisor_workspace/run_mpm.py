#!/usr/bin/env python3
"""
Deal Advisor: PT Mandala Prima Makmur — Deep Due Diligence
Uses real data from investor presentation, DD checklist, and audited financials.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from deal_advisor.schemas import (
    DealResearchRequest, DealScoreCard, DimensionScore,
    DealMemo, Source, DealType, ResearchDepth
)
from deal_advisor.memo_writer import render_markdown, _score_table
from datetime import datetime, timezone

# ─── BUILD REQUEST ───────────────────────────────────────────
request = DealResearchRequest(
    target="PT Mandala Prima Makmur",
    sector="Cocoa Processing & Chocolate Manufacturing",
    deal_type=DealType.PUBLIC_COMPANY,
    research_depth=ResearchDepth.DEEP,
    investment_question="Should we invest in / lend to MPM for growth capex and working capital?",
    regions=["Indonesia", "ASEAN", "Global"],
    comparables=[
        "Barry Callebaut Indonesia",
        "Cargill Cocoa",
        "Olam Cocoa",
        "BT Cocoa",
        "Freyabadi Indotama",
        "Petra Foods"
    ],
    custom_context="""PT Mandala Prima Makmur (MPM) adalah perusahaan pengolahan kakao dan manufaktur coklat yang didirikan tahun 2001, berkantor pusat di Tangerang, Banten. Revenue 2025: Rp 57.3B (-14% YoY vs Rp 66.7B), Net Profit Rp 16.4B (+32% YoY), margin 28.6%. Total Aset Rp 76.9B, Ekuitas Rp 38.9B (+150%). 74 karyawan. Sertifikasi: Halal, ISO 9001:2015, FSSC 22000, US FDA, KOSHER, HACCP. Produk: cocoa powder (DRITTO, DIVES, KLACOKLAT, REVOCO), chocolate spread, premium drinks (Prospero Realcho), dark chocolate 85%, couverture, freeze-dried (BELILAGI), vacuum fried chips. Pemegang saham: PT Mandala Multi Cipta 60.74%, PT Prosperio Golden Makmur 39.05%. Sedang mencari pendanaan via SIB Mandala Bhavana untuk capex mesin dan working capital."""
)

# ─── BUILD SCORECARD WITH REAL DATA ──────────────────────────
scorecard = DealScoreCard(
    market_opportunity=DimensionScore(
        name="Market Opportunity",
        score=7.0,
        confidence=0.72,
        evidence=[
            "Indonesia produsen kakao #3 dunia setelah Ivory Coast dan Ghana",
            "Konsumsi coklat domestik tumbuh seiring middle class expansion",
            "Sertifikasi Halal membuka pasar ASEAN & Timur Tengah senilai miliaran dolar",
            "FSSC 22000 + US FDA membuka pasar ekspor premium (US, EU, Jepang)",
            "Global cocoa powder market projected 4.5% CAGR to 2030"
        ],
        risks=[
            "Pasar cocoa processing Indonesia mature — growth harus dari ekspor",
            "Revenue decline -14% menunjukkan tekanan demand/competitive",
            "Kakao Indonesia menghadapi isu produktivitas (aging trees, penyakit)"
        ]
    ),

    team_quality=DimensionScore(
        name="Team Quality",
        score=5.0,
        confidence=0.40,
        evidence=[
            "24 tahun operating history membuktikan kemampuan eksekusi",
            "Struktur 100% corporate ownership (bukan family feud prone)",
            "74 karyawan untuk Rp 57B revenue menunjukkan operasi lean & efisien"
        ],
        risks=[
            "Limited visibility ke tim manajemen — no bios, no track record details",
            "Key person risk: organisasi kecil, tidak jelas succession plan",
            "Data management tim tidak tersedia di DD checklist (kosong)",
            "Rp 774M revenue/employee sangat tinggi — perlu dikonfirmasi model bisnis"
        ]
    ),

    product_strength=DimensionScore(
        name="Product Strength",
        score=7.5,
        confidence=0.65,
        evidence=[
            "Portfolio 7 kategori produk — cocoa powder, spread, drinks, dark choc, couverture, freeze-dried, chips",
            "Dark Chocolate 85% menunjukkan kapabilitas R&D dan inovasi produk",
            "Freeze-dried products (BELILAGI) — kategori premium high-margin",
            "9 sertifikasi internasional (FSSC 22000, US FDA, KOSHER, HACCP, SNI, dll)",
            "Brand consumer established: DRITTO, DIVES, KLACOKLAT, REVOCO"
        ],
        risks=[
            "Cocoa powder adalah semi-komoditas — diferensiasi terbatas di B2B",
            "Brand recognition masih lokal/regional, bukan nasional apalagi global",
            "Tidak jelas proporsi B2B vs B2C revenue — margin profile berbeda signifikan"
        ]
    ),

    traction=DimensionScore(
        name="Traction & Growth",
        score=4.5,
        confidence=0.50,
        evidence=[
            "Revenue Rp 57.3B menunjukkan skala bisnis yang meaningful",
            "Net profit margin 28.6% adalah exceptional — efisiensi operasional tinggi",
            "Multi-channel: B2B industrial + branded consumer (e-commerce, modern trade) + export"
        ],
        risks=[
            "Revenue turun -14% YoY — red flag utama, trajectory negatif",
            "Tidak ada data customer concentration — risk kehilangan 1-2 big buyers",
            "Tidak ada visibility sales pipeline atau order book",
            "Belum jelas split revenue: domestic vs export, B2B vs B2C"
        ]
    ),

    competitive_moat=DimensionScore(
        name="Competitive Moat",
        score=6.5,
        confidence=0.60,
        evidence=[
            "9 sertifikasi internasional adalah barrier to entry signifikan (FSSC 22000 butuh investasi besar)",
            "24 tahun relationship dengan supplier kakao dan buyer",
            "Brand consumer portfolio memberi pricing power vs pure commodity player",
            "US FDA + KOSHER membuka pasar yang tidak accessible bagi pemain tanpa sertifikasi"
        ],
        risks=[
            "Bersaing dengan Barry Callebaut, Cargill, Olam — pemain global dengan skala 100x+",
            "B2B cocoa processing adalah industri dengan switching cost rendah",
            "No patents atau proprietary technology teridentifikasi",
            "Moat bergantung pada sertifikasi dan relationship — bisa direplikasi dengan modal"
        ]
    ),

    financial_health=DimensionScore(
        name="Financial Health",
        score=8.0,
        confidence=0.68,
        evidence=[
            "Net profit margin 28.6% — exceptional untuk food manufacturing (avg industri ~5-10%)",
            "Net profit Rp 16.4B, pertumbuhan +32% YoY",
            "Ekuitas Rp 38.9B — equity buffer sangat kuat, debt capacity besar",
            "Capital injection ~Rp 7B dari PT Prosperio Golden Makmur — confidence signal dari investor strategis",
            "Cash flow positif (implied dari profitabilitas dan restrukturisasi)"
        ],
        risks=[
            "Revenue contraction -14% — jika berlanjut, profitabilitas akan tertekan",
            "Laporan keuangan 2024 hanya 'review + kompilasi', bukan full audit — data reliability concern",
            "Tidak tersedia aging AR/AP — working capital risk tidak terukur",
            "Cocoa price spike 2024 menguntungkan processor dengan inventory — apakah sustainable?"
        ]
    ),

    risk_profile=DimensionScore(
        name="Risk Profile",
        score=5.5,
        confidence=0.55,
        evidence=[
            "Ekuitas Rp 38.9B memberi buffer terhadap commodity price shock",
            "Diversifikasi 7 kategori produk mengurangi single-product dependency",
            "Sertifikasi internasional mengurangi regulatory risk untuk ekspor"
        ],
        risks=[
            "Cocoa price volatility — raw material 40-60% COGS, harga kakao naik 200%+ di 2024",
            "Konsentrasi kepemilikan: 2 pemegang saham kontrol 99.78% — minority protection risk",
            "Rupiah depreciation risk pada imported equipment & beans",
            "Laporan keuangan bukan full audit — risiko kualitas data",
            "Revenue decline trajectory — apakah temporer atau struktural?",
            "Organisasi kecil (74 orang) — operational resilience risk"
        ]
    )
)

# ─── BUILD DEAL MEMO WITH RICH CONTENT ─────────────────────────
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

memo = DealMemo(
    title="Deal Memo: PT Mandala Prima Makmur — Cocoa Processing Growth Investment",

    executive_summary=(
        "PT Mandala Prima Makmur (MPM) is a 24-year-old Indonesian cocoa processor and chocolate manufacturer "
        "evaluated for growth capital investment. The company shows **exceptional profitability** with 28.6% net margin "
        "and Rp 16.4B net profit on Rp 57.3B revenue, supported by a strong equity base of Rp 38.9B after a 2025 "
        "restructuring. However, revenue declined -14% YoY — a critical red flag that demands investigation. "
        "International certifications (FSSC 22000, US FDA, KOSHER) position MPM for export growth. "
        f"Overall score: **{scorecard.overall_score}/10** — **{scorecard.recommendation}** "
        f"(confidence: {scorecard.overall_confidence:.2f}). The thesis hinges on whether the revenue decline is "
        "temporary (commodity price pass-through) or structural (market share loss)."
    ),

    company_overview=(
        "**PT Mandala Prima Makmur** was founded in 2001 and is headquartered in Tangerang, Banten, Indonesia. "
        "The company operates in the cocoa processing and chocolate manufacturing industry with 74 employees. "
        "Revenue reached Rp 57.3B in 2025. MPM holds 9 international quality certifications and serves "
        "B2B industrial, branded consumer (e-commerce, modern trade), and export markets.\n\n"
        "**Key Brands:** DRITTO, DIVES, KLACOKLAT, REVOCO (cocoa powder); MILECOCO, COLECO, COKICO, VELSON (spreads); "
        "Prospero Realcho (premium drinks); BELILAGI (freeze-dried).\n\n"
        "**Shareholders:** PT Mandala Multi Cipta (60.74%), PT Prosperio Golden Makmur (39.05%). "
        "PT Prosperio entered in 2025 with a ~Rp 7B capital injection, marking a major corporate restructuring."
    ),

    market_analysis=(
        "**Indonesia Cocoa Industry Position:** Indonesia is the world's 3rd largest cocoa bean producer after "
        "Ivory Coast and Ghana. Domestic processing capacity is ~800,000 tons/year. However, downstream processing "
        "is dominated by 5-6 multinational players (Barry Callebaut, Cargill, Olam). MPM operates as a mid-tier "
        "processor with strong domestic consumer brands.\n\n"
        "**Demand Drivers:**\n"
        "- Growing Indonesian middle class driving chocolate consumption (+6-8% CAGR)\n"
        "- Halal certification opens $2T+ Muslim consumer market across ASEAN and Middle East\n"
        "- Global cocoa powder market projected at 4.5% CAGR through 2030\n"
        "- Health trend: dark chocolate 85% and freeze-dried products align with premium health segment\n\n"
        "**Supply Dynamics:** Global cocoa prices surged +200% in 2024 due to West Africa supply shortages "
        "(Ivory Coast/Ghana crop diseases, weather). This benefits processors holding inventory at lower cost "
        "basis, but creates working capital pressure. Indonesia's domestic cocoa production has been declining "
        "due to aging trees and pod borer disease — increasing reliance on imports.\n\n"
        "**MPM Position:** Revenue decline -14% is concerning. If driven by volume loss, it signals competitive "
        "pressure. If driven by cocoa price pass-through (lower prices in 2025 vs peak 2024), it's less alarming. "
        "The 28.6% margin suggests MPM has pricing power or cost advantages. Without detailed revenue breakdown "
        "by product/channel, the market position assessment carries medium confidence."
    ),

    competitive_landscape=(
        "**Competitive Set:**\n\n"
        "1. **Barry Callebaut** — Global #1 chocolate manufacturer, significant Indonesian presence. "
        "Scale 100x MPM. Primarily B2B industrial. Not competing in Indonesian consumer brands.\n"
        "2. **Cargill Cocoa** — Global agribusiness giant, major Indonesian cocoa processor. "
        "B2B focus, commodity-scale operations.\n"
        "3. **Olam Cocoa** (ofi) — Global cocoa bean trader and processor. Strong in Asian sourcing.\n"
        "4. **BT Cocoa** — Indonesian mid-tier processor, similar scale to MPM. Major competitor.\n"
        "5. **Freyabadi Indotama** — Indonesian cocoa processor, Barry Callebaut subsidiary.\n"
        "6. **Petra Foods** — Singapore-listed, strong in SEA consumer chocolate brands.\n\n"
        "**MPM's Competitive Position:**\n"
        "MPM differentiates through its **dual B2B + branded consumer model**. While multinationals dominate "
        "industrial cocoa processing, MPM's consumer brands (DRITTO, KLACOKLAT) give it a retail presence "
        "that pure B2B players lack. The 9 international certifications create a moat against smaller local "
        "processors who can't afford the compliance investment. However, against global players, MPM's scale "
        "disadvantage is significant — winning on service, flexibility, and domestic market knowledge, not on cost."
    ),

    business_model=(
        "**Revenue Mix (estimated, not disclosed):**\n"
        "- B2B Industrial: Cocoa powder, couverture, compound to food manufacturers — lower margin, volume-driven\n"
        "- Branded Consumer: DRITTO, KLACOKLAT, Prospero Realcho via e-commerce and modern trade — higher margin\n"
        "- Export: Leveraging US FDA + KOSHER for premium markets — highest potential margin\n\n"
        "**Cost Structure:**\n"
        "Cocoa beans represent an estimated 40-60% of COGS, making MPM highly sensitive to commodity prices. "
        "Processing costs (labor, energy, packaging) are the remainder. With only 74 employees and Rp 57.3B "
        "revenue (Rp 774M/employee), the business appears highly automated or uses a toll-manufacturing model.\n\n"
        "**Capital Intensity:**\n"
        "The company is seeking capex financing for new machinery, suggesting equipment upgrades needed for "
        "growth or efficiency. Working capital requirements are high due to cocoa bean inventory costs.\n\n"
        "**Key Question:** Is the 28.6% margin sustainable, or was 2025 an anomaly from inventory gains "
        "during the cocoa price surge?"
    ),

    team_analysis=(
        "**Limited Information Available (Low Confidence):**\n\n"
        "The DD checklist from Naiman Global shows that Section F (Organization & Legal) remains largely "
        "unfilled. No management bios, org chart, or key person details were provided in the investor "
        "presentation or supporting documents.\n\n"
        "**What We Know:**\n"
        "- 74 total employees across all functions\n"
        "- 100% corporate ownership structure (no individual/family shareholders)\n"
        "- 24 years of continuous operation suggests management stability\n"
        "- The capital restructuring (bringing in PT Prosperio Golden Makmur) implies professional management\n\n"
        "**Information Gaps (Required Before Investment Decision):**\n"
        "- CEO and key management backgrounds, industry experience\n"
        "- Succession planning — organization is small, key person risk is high\n"
        "- Board composition and governance practices\n"
        "- Employee turnover and culture indicators\n\n"
        "**Assessment:** This dimension carries the lowest confidence (0.40). The lean structure (74 people for "
        "Rp 57B revenue) could indicate either superb operational efficiency or under-investment in talent. "
        "Due diligence MUST include management interviews and reference checks."
    ),

    financial_overview=(
        "**Key Financial Data (from Investor Presentation 2025):**\n\n"
        "| Metric | 2025 | 2024 | Change |\n"
        "|---|---:|---:|---:|\n"
        "| Revenue | Rp 57.3B | Rp 66.7B | -14% |\n"
        "| Net Profit | Rp 16.4B | Rp 12.4B | +32% |\n"
        "| Total Assets | Rp 76.9B | Rp 50.4B | +53% |\n"
        "| Total Equity | Rp 38.9B | Rp 15.6B | +150% |\n"
        "| Net Margin | 28.6% | 18.6% | +10pp |\n\n"
        "**Analysis:**\n"
        "- Revenue decline with profit growth = significant margin expansion. This could be driven by (a) product "
        "mix shift to higher-margin products, (b) inventory gains from cocoa price surge, (c) cost cutting.\n"
        "- Equity jump of +150% = ~Rp 7B new capital injection + Rp 16.4B retained profits. Very strong balance sheet.\n"
        "- Asset growth +53% = major investment in fixed assets or working capital.\n\n"
        "**Data Quality Note:** The 2024 financial statements were prepared under a 'review + compilation' engagement "
        "with KAP TERA, NOT a full audit. An independent auditor was to be appointed separately. This is a "
        "significant concern — financial data reliability is lower than for a fully audited company. "
        "Investors should request full audit or at minimum an independent accountant's report.\n\n"
        "**Missing Critical Data:**\n"
        "- Cash flow statements (operating, investing, financing breakdown)\n"
        "- Debt schedule (existing loans, interest rates, maturities, covenants)\n"
        "- Revenue breakdown by product/customer/channel\n"
        "- Working capital details (AR aging, AP aging, inventory composition)"
    ),

    traction_metrics=(
        "**Customer & Sales Data (from DD Checklist):**\n\n"
        "Section D (Customer & Sales Data) is marked as IMPORTANT but largely incomplete in the DD checklist. "
        "The following data is MISSING and required for investment decision:\n\n"
        "- Top 20 customer list with revenue contribution\n"
        "- Sales by channel (% modern trade vs traditional vs export)\n"
        "- Product-level revenue, pricing, and margin\n"
        "- Sales targets 2026-2028\n"
        "- New product pipeline timeline\n\n"
        "**Production Data:**\n"
        "Section B (Production & Capacity) is also incomplete. Missing: machine list, utilization rates, "
        "actual monthly output, production costs per unit, yield rates.\n\n"
        "**What We Can Infer:**\n"
        "- Revenue scale of Rp 57.3B suggests meaningful market presence\n"
        "- 28.6% margin suggests strong customer relationships and pricing power\n"
        "- Multiple sales channels (B2B, e-commerce, export) reduce dependency on any single channel\n"
        "- The company survived 2024's cocoa price crisis, indicating operational resilience\n\n"
        "**Assessment:** Traction metrics carry low confidence (0.50) due to data gaps. The DD process must "
        "prioritize collecting customer concentration data and production KPIs."
    ),

    risk_analysis=(
        "**Risk Matrix (High to Low Severity):**\n\n"
        "🔴 **HIGH — Revenue Contraction Trajectory**\n"
        "-14% revenue decline is the single biggest risk. Without understanding the root cause (volume vs price, "
        "customer loss vs market contraction), the growth thesis is unvalidated. If decline continues, even "
        "high margins won't protect equity value.\n\n"
        "🔴 **HIGH — Cocoa Price Volatility**\n"
        "Cocoa beans are 40-60% of COGS. Global prices surged 200%+ in 2024 due to West Africa supply crisis. "
        "MPM benefited in 2025 (margin expansion from lower-cost inventory), but the reverse is possible. "
        "A price collapse would hurt inventory values; a further spike would crush working capital.\n\n"
        "🟡 **MEDIUM — Data Quality / Audit Risk**\n"
        "2024 financials are not fully audited. KAP TERA performed review + compilation only. Full audit was "
        "\"to be appointed.\" This is unusual for a company of this scale seeking external investment. "
        "Historical financials may not be reliable.\n\n"
        "🟡 **MEDIUM — Ownership Concentration**\n"
        "Two shareholders control 99.78%. No minority protections visible. If PT Mandala Multi Cipta and "
        "PT Prosperio Golden Makmur disagree, the company is paralyzed. Exit options for minority investors "
        "are limited.\n\n"
        "🟡 **MEDIUM — Competitive Pressure**\n"
        "Global players (Barry Callebaut, Cargill, Olam) have 100x+ scale. They can underprice MPM in B2B. "
        "MPM's defense is branded consumer products and service — defensible but not impenetrable.\n\n"
        "🟢 **LOW — FX and Import Risk**\n"
        "Rupiah depreciation increases cost of imported beans and equipment. Partially hedged by export revenue. "
        "Indonesia's domestic cocoa production is declining, increasing import dependency — structural FX exposure."
    ),

    investment_thesis=(
        "**The Bull Case (Score 7.5-8.0):**\n"
        "MPM is a hidden gem — a 24-year profitable cocoa processor with industry-leading margins and "
        "international certifications that unlock export growth. The revenue decline is temporary "
        "(cocoa price pass-through effect), and the underlying volume is stable or growing. "
        "With new capex, MPM doubles capacity and captures ASEAN/Middle East export demand. "
        "The 28.6% margin is sustainable because it reflects MPM's branded consumer product mix, "
        "not just commodity processing. The 2025 restructuring brought in a strategic investor "
        "who will professionalize management and drive growth. Target: 3-5x return in 5 years "
        "through combination of profit growth and multiple expansion.\n\n"
        "**The Bear Case (Score 3.0-4.5):**\n"
        "MPM is a cocoa processor in a commodity industry with no sustainable moat. The 28.6% margin "
        "is a one-time event driven by inventory gains during the 2024 cocoa price spike — normalize "
        "this and MPM is a 10-15% margin business at best. Revenue decline is structural: MPM is losing "
        "B2B customers to Barry Callebaut and Cargill who have better pricing. The financials aren't even "
        "fully audited — who knows what's really in the books? Two shareholders control everything and "
        "the fundraising is dilution in disguise. The cocoa price cycle will reverse and crush margins. "
        "Avoid.\n\n"
        "**Our Base Case (Score 6.56/10 — HOLD):**\n"
        "MPM has genuine strengths: exceptional margins (even if partially cycle-driven), international "
        "certifications, diversified products, and a strong balance sheet. However, the revenue decline "
        "and data gaps prevent a BUY recommendation at this stage. The investment is interesting but "
        "requires answers to critical questions first:\n\n"
        "1. **Revenue decline root cause** — volume or price? Customer loss or market contraction?\n"
        "2. **Full audit** — request audited financials before proceeding\n"
        "3. **Customer concentration** — who are top 10 customers and what % of revenue?\n"
        "4. **Management depth** — who runs this company beyond the shareholders?\n"
        "5. **Use of proceeds detail** — what specific machinery, capacity increase, revenue impact?\n\n"
        "*Answer these and the score could move to BUY (7.0+) or PASS (<5.5).*"
    ),

    recommendation=scorecard.recommendation,
    scorecard=scorecard,
    sources=[
        Source(
            url="https://docs.google.com/presentation/d/13p3bWtfs25w07A4xGy6ZUdrgM8GwpaHj",
            title="PT Mandala Prima Makmur — Investor Presentation 2025",
            snippet="Executive summary, financial performance (2024-2025), product portfolio, certifications, shareholder structure, capital restructuring details, contact information.",
            relevance=0.95,
            source_type="primary"
        ),
        Source(
            url="https://docs.google.com/spreadsheets/d/1jrGOsFMgRG9DofD1FDNWFDk1AWYJZnPh",
            title="DD Checklist — Mandala Prima Makmur (Naiman Global)",
            snippet="Due diligence checklist covering 6 categories: Financial Statements, Production & Capacity, Use of Proceeds, Customer & Sales, Supplier & Raw Materials, Organization & Legal.",
            relevance=0.90,
            source_type="primary"
        ),
        Source(
            url="https://drive.google.com/file/d/1RH6QWdLQ-f2VdrTFyeUlrkhUR-QWsjaM",
            title="Laporan Keuangan 2024 — PT Mandala Prima Makmur (KAP TERA)",
            snippet="Financial statements for year ended Dec 31, 2024. Review + compilation engagement (NOT full audit). Rp 115M fee. KAP TERA, Cyber 2 Tower, Jakarta.",
            relevance=0.85,
            source_type="primary"
        ),
        Source(
            url="https://docs.google.com/document/d/12uPfAkIJx08xXg916gmfgt5GcaTv9a9W",
            title="Penawaran SIB Mandala Bhavana 061125",
            snippet="SIB (Securities Issuance) offering document for Mandala Bhavana investment vehicle. November 2025.",
            relevance=0.75,
            source_type="primary"
        ),
        Source(
            url="https://drive.google.com/file/d/10MJ9GDDEfJaPWhtPX_lyQRUhvz7BY5_I",
            title="RUPS PT Mandala Prima Makmur",
            snippet="General shareholders meeting documentation — resolutions and shareholder decisions.",
            relevance=0.70,
            source_type="primary"
        ),
        Source(
            url="local://deal-advisor-engine",
            title="Deal Advisor Intelligence Engine — Dimension Scoring",
            snippet=f"7-dimension analysis: Market (7.0), Team (5.0), Product (7.5), Traction (4.5), Moat (6.5), Financial (8.0), Risk (5.5). Weighted score: {scorecard.overall_score}/10.",
            relevance=1.0,
            source_type="internal"
        )
    ],
    research_questions=[
        "What drove MPM's -14% revenue decline in 2025 — volume loss, price decline, or customer churn?",
        "Who are MPM's top 10 customers and what % of total revenue do they represent?",
        "What is MPM's revenue split: domestic vs export, B2B vs B2C, by product category?",
        "Is the 28.6% net margin sustainable, or was it inflated by cocoa price cycle inventory gains?",
        "What is MPM's existing debt — amount, interest rates, maturity profile, covenants?",
        "Who is the management team — CEO, COO, CFO backgrounds and industry experience?",
        "What specific machinery will the capex fund, what capacity increase, and what is the expected ROI?",
        "How does MPM's cocoa bean sourcing work — % domestic vs imported, supplier concentration?",
        "What is MPM's actual production capacity and current utilization rate?",
        "How does MPM's pricing compare to Barry Callebaut and BT Cocoa in the Indonesian market?"
    ],
    token_usage_estimate=12600000
)

# ─── RENDER AND SAVE ─────────────────────────────────────────
markdown = render_markdown(memo)

output_dir = Path(__file__).resolve().parent / "mpm_db"
output_dir.mkdir(parents=True, exist_ok=True)

out_path = output_dir / "mandala_prima_makmur_deal_memo.md"
out_path.write_text(markdown)

print(f"MEMO WRITTEN: {out_path}")
print(f"\n{'='*60}")
print(f"PT MANDALA PRIMA MAKMUR — DEAL ADVISOR SCORECARD")
print(f"{'='*60}")
print(f"Overall Score: {scorecard.overall_score}/10")
print(f"Confidence:    {scorecard.overall_confidence:.2f}")
print(f"Recommendation: {scorecard.recommendation}")
print(f"\nDimensions:")
for d in scorecard.dimensions():
    bar = "█" * int(d.score) + "░" * (10 - int(d.score))
    print(f"  {d.name:<25s} {bar} {d.score:.1f}/10  (conf: {d.confidence:.2f})")
print(f"\nKey Risks:")
for r in memo.risk_analysis.split("\n")[:4]:
    if r.strip():
        print(f"  {r.strip()}")
print(f"\nKey Thesis:")
print(f"  {memo.investment_thesis[:200]}...")
