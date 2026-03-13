# 银行股分红分析工具

一个用于分析A股银行股分红数据的Python脚本，特别适合价值投资者和程序员投资者使用。

## 功能特点

- 📊 **全面分析**：支持10+家A股主要银行股
- 📈 **多指标计算**：股息率、分红率、增长率等关键指标
- 📉 **可视化展示**：自动生成专业分析图表
- 📝 **报告生成**：输出Markdown格式分析报告
- 🔌 **多数据源**：支持yfinance、tushare，自动降级到模拟数据
- 🎯 **易于扩展**：模块化设计，方便添加新功能

## 快速开始

### 1. 安装依赖
```bash
# 基础依赖
pip install pandas numpy matplotlib

# 数据源（至少安装一个）
pip install yfinance      # 国际数据源（推荐）
# 或
pip install tushare       # 国内数据源（需要token）

# 可选：增强功能
pip install seaborn plotly jupyter
```

### 2. 运行脚本
```bash
# 下载脚本
git clone https://github.com/AMDvsTMD/bank-stock-analysis.git
cd bank-stock-analysis

# 运行分析
python bank_stock_dividend_analysis.py
```

### 3. 查看结果
脚本运行后将生成：
- `bank_analysis_results.png` - 分析图表
- `bank_analysis_report.md` - 详细分析报告

## 使用示例

### 基础使用
```python
from bank_stock_dividend_analysis import BankStockAnalyzer

# 创建分析器
analyzer = BankStockAnalyzer(use_real_data=True)

# 分析所有银行股
results = analyzer.analyze_all_banks()

# 显示结果
print(results[['name', 'dividend_yield', 'latest_dividend']].head())
```

### 单只股票分析
```python
# 深度分析招商银行
cmb_data = analyzer.fetch_real_data('600036.SS')
cmb_metrics = analyzer.calculate_metrics(cmb_data)

print(f"招商银行股息率: {cmb_metrics['dividend_yield']}%")
print(f"最新分红: {cmb_metrics['latest_dividend']}元/股")
```

### 自定义可视化
```python
# 生成自定义图表
analyzer.visualize_results(
    results, 
    save_path='custom_analysis.png'
)
```

### 生成详细报告
```python
# 生成分析报告
analyzer.generate_report(
    results,
    output_file='my_investment_report.md'
)
```

## 支持的银行股

| 股票代码 | 银行名称 | 备注 |
|---------|---------|------|
| 600036.SS | 招商银行 | 股份制银行龙头 |
| 601398.SS | 工商银行 | 国有大行 |
| 601939.SS | 建设银行 | 国有大行 |
| 601288.SS | 农业银行 | 国有大行 |
| 601988.SS | 中国银行 | 国有大行 |
| 601328.SS | 交通银行 | 国有大行 |
| 600000.SS | 浦发银行 | 股份制银行 |
| 601166.SS | 兴业银行 | 股份制银行 |
| 600016.SS | 民生银行 | 股份制银行 |
| 600919.SS | 江苏银行 | 城商行 |

## 分析指标说明

### 核心指标
1. **股息率** = 每股分红 / 股价 × 100%
   - 衡量现金回报率
   - 通常越高越好，但需结合公司基本面

2. **分红率** = 每股分红 / 每股收益 × 100%
   - 衡量分红占利润的比例
   - 30%-60%为健康范围

3. **分红增长率** = (今年分红 - 去年分红) / 去年分红 × 100%
   - 衡量分红增长趋势
   - 持续正增长为佳

### 辅助指标
- **当前股价**：最新收盘价
- **每股分红**：最新年度每股分红金额
- **每股收益**：每股盈利（如有）

## 高级功能

### 添加新的银行股
```python
# 在BankStockAnalyzer类的__init__方法中添加
self.bank_stocks['601998.SS'] = '中信银行'
self.bank_stocks['601009.SS'] = '南京银行'
```

### 自定义分析指标
```python
class EnhancedAnalyzer(BankStockAnalyzer):
    """扩展的分析器"""
    
    def calculate_pe_ratio(self, stock_data):
        """计算市盈率"""
        eps = stock_data.get('eps')
        price = stock_data.get('stock_price')
        return price / eps if eps and eps > 0 else None
    
    def calculate_pb_ratio(self, stock_data):
        """计算市净率"""
        bps = stock_data.get('bps')  # 每股净资产
        price = stock_data.get('stock_price')
        return price / bps if bps and bps > 0 else None
```

### 数据源配置
```python
# 使用tushare（需要token）
import tushare as ts
ts.set_token('你的tushare_token')

# 使用yfinance配置
import yfinance as yf
yf.pdr_override()  # 兼容pandas_datareader
```

## 常见问题

### Q1: 运行时报错"ModuleNotFoundError"
**A**: 安装缺失的依赖库：
```bash
pip install pandas numpy matplotlib yfinance
```

### Q2: 如何获取真实数据？
**A**: 两种方式：
1. 使用yfinance（自动支持A股）：
   ```python
   analyzer = BankStockAnalyzer(use_real_data=True)
   ```
2. 使用tushare（需注册获取token）：
   ```python
   import tushare as ts
   ts.set_token('your_token')
   ```

### Q3: 数据更新频率？
**A**: 
- 股价数据：实时（取决于数据源）
- 分红数据：年度（财报公布后更新）
- 建议每周运行一次更新分析

### Q4: 如何添加其他行业股票？
**A**: 修改`bank_stocks`字典，添加其他股票代码和名称。

## 投资建议（仅供参考）

1. **高股息策略**：关注股息率>5%的银行股
2. **增长策略**：关注分红增长率>5%的银行股  
3. **平衡策略**：股息率4-6% + 正增长
4. **风险提示**：银行股受宏观经济、政策影响较大

## 开发计划

- [ ] 添加更多技术指标（MACD、RSI等）
- [ ] 支持港股、美股银行股
- [ ] 添加自动化邮件报告功能
- [ ] 开发Web界面（Streamlit/Flask）
- [ ] 集成回测功能

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

MIT License

## 免责声明

本工具仅用于学习和研究目的，不构成投资建议。投资者应独立判断，自负风险。作者不对因使用本工具造成的任何损失负责。

## 关注公众号

![公众号二维码](qrcode.jpg)

**公众号：程序员的价投之路**  
**专注：程序员思维 × 价值投资**  
**理念：用代码的严谨，做价值的守护**

扫描二维码关注，获取：
- 📈 最新银行股分析
- 💻 Python投资工具
- 🧠 程序员价投心得
- 📊 独家数据分析

---

*投资有风险，入市需谨慎*