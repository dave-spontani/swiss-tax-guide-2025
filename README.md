# 🇨🇭 Swiss Tax Guide 2025 - Interactive Streamlit App

A comprehensive, interactive web application for understanding and calculating Swiss taxes across all 26 cantons.

![Swiss Flag](https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Flag_of_Switzerland_%28Pantone%29.svg/320px-Flag_of_Switzerland_%28Pantone%29.svg.png)

## 🌟 Features

### 📊 Tax Calculator
- Calculate federal, cantonal, and municipal taxes
- Support for single and married taxpayers
- Real-time deduction calculations
- Visual breakdown of tax components

### 🗺️ Canton Comparison
- Compare all 26 Swiss cantons
- Interactive tax rate visualizations
- Wealth tax comparison
- Savings calculator between cantons

### ✅ Deductions Checklist
- Comprehensive checklist of all deductions
- Categories: Professional, Personal, Real Estate, and Commonly Forgotten
- Real-time calculation of total deductions and savings
- Track your tax optimization progress

### 🏦 Pillar 3a Guide
- Contribution limit calculator
- Tax savings estimation
- 30-year investment projection
- Interactive growth visualization

### 📈 Investment Income
- Capital gains tax rules (tax-free for private investors!)
- Dividend taxation calculator
- Wealth tax calculator
- Private investor qualification checker

### 🏠 Real Estate Tax
- Current Eigenmietwert system calculator
- New 2028 reform information
- Side-by-side comparison
- First-time buyer transitional benefits

## 🚀 Quick Start

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/swiss-tax-guide-2025.git
cd swiss-tax-guide-2025
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run swiss_tax_app.py
```

4. Open your browser at `http://localhost:8501`

## 📋 Requirements

- Python 3.8 or higher
- streamlit 1.31.1
- pandas 2.2.0
- plotly 5.18.0

## 📖 Documentation

This app is based on the complete Swiss Tax Guide 2025, which covers:

- **Federal Tax System**: Progressive tax brackets up to 11.5%
- **Cantonal Variations**: Tax rates from 22.2% (Zug) to 45% (Geneva)
- **Municipal Multipliers**: How local taxes work
- **Pillar 3a**: Maximum CHF 7,258 deduction for 2025
- **Capital Gains**: Tax-free for private investors
- **Wealth Tax**: 0.1% to 0.88% depending on canton
- **2025 Eigenmietwert Reform**: Major changes to homeowner taxation

## 🎯 Key Insights

- Switzerland has a **3-tier tax system** (federal, cantonal, municipal)
- **Location matters hugely**: 22-45% total tax burden depending on canton
- **Pillar 3a** is the #1 tax deduction (100% deductible)
- **Capital gains are tax-free** for private investors (huge advantage!)
- **Wealth tax** exists in Switzerland (0.3-0.7% typical range)
- **Eigenmietwert reform** coming in 2028

## 📊 Canton Tax Rates (2025)

| Rank | Canton | Max Tax Rate |
|------|--------|--------------|
| 1 | Zug | 22.2% |
| 2 | Schwyz | 22.59% |
| 3 | Appenzell Innerrhoden | 23.8% |
| ... | ... | ... |
| 24 | Vaud | 41.5% |
| 25 | Basel-Landschaft | 42.2% |
| 26 | Geneva | 45.0% |

## 🛠️ Technologies Used

- **Streamlit**: Interactive web framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Python**: Backend logic and calculations

## 📁 Project Structure

```
swiss-tax-guide-2025/
│
├── swiss_tax_app.py           # Main Streamlit application
├── swiss_tax_guide_complete.md # Complete tax guide documentation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 💡 Usage Tips

1. **Tax Calculator**: Input your income and deductions to see your exact tax burden
2. **Canton Comparison**: Compare 2-5 cantons to find the best location for your situation
3. **Deductions Checklist**: Use before filing to ensure you don't miss any deductions
4. **Pillar 3a Guide**: See the long-term impact of maximizing your contributions
5. **Investment Income**: Check if you qualify as a private investor for tax-free gains

## ⚠️ Disclaimer

This tool is for **informational purposes only**. Tax laws change frequently and individual situations vary. Always consult a qualified tax advisor for personalized advice.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Data sourced from Swiss Federal Tax Administration (ESTV)
- Canton information from official cantonal tax authorities
- Tax rates verified against multiple sources (see documentation)

---

**Last Updated**: December 2025

**Note**: Tax information is current as of 2025. Please verify rates and regulations with official sources.

## 🔗 Useful Links

- [Swiss Federal Tax Administration (ESTV)](https://www.estv.admin.ch)
- [Official Tax Calculator](https://www.estv.admin.ch/estv/en/home/fta/tax-statistics/calculate-taxes.html)
- [Comparis Tax Comparison](https://en.comparis.ch/steuern/steuervergleich/steuerrechner)
- [Swiss Tax Map](https://www.swisstaxmap.ch/)

---

Made with ❤️ for the Swiss tax community
