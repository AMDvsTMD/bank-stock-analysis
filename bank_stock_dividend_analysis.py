#!/usr/bin/env python3
"""
银行股分红数据分析脚本
用于分析A股银行股的分红率、股息率等关键指标

作者：程序员的价投之路
公众号：程序员的价投之路
GitHub：https://github.com/AMDvsTMD/bank-stock-analysis

依赖：
    pip install pandas numpy matplotlib yfinance tushare
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
import warnings
import os
import platform
warnings.filterwarnings('ignore')

# 设置中文字体，解决中文乱码问题
def setup_chinese_font():
    """配置matplotlib使用中文字体"""
    system = platform.system()
    
    # 常见中文字体列表，按优先级排序
    chinese_fonts = [
        # macOS 字体
        'PingFang SC',  # 苹方
        'Hiragino Sans GB',  # 冬青黑体
        'STHeiti',  # 华文黑体
        'STSong',  # 华文宋体
        # Windows 字体
        'Microsoft YaHei',  # 微软雅黑
        'SimHei',  # 黑体
        'SimSun',  # 宋体
        'KaiTi',  # 楷体
        # Linux 字体
        'WenQuanYi Micro Hei',  # 文泉驿微米黑
        'WenQuanYi Zen Hei',  # 文泉驿正黑
        'DejaVu Sans',  # 备用
    ]
    
    # 设置字体
    try:
        # 方法1: 使用系统已有字体
        matplotlib.rcParams['font.sans-serif'] = chinese_fonts
        
        # 方法2: 添加字体路径（如果需要）
        if system == 'Darwin':  # macOS
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',
                '/System/Library/Fonts/STHeiti Medium.ttc',
                '/Library/Fonts/Microsoft/微软雅黑.ttf',
            ]
        elif system == 'Windows':
            font_paths = [
                'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
                'C:/Windows/Fonts/simhei.ttf',  # 黑体
                'C:/Windows/Fonts/simsun.ttc',  # 宋体
            ]
        else:  # Linux
            font_paths = [
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            ]
        
        # 尝试添加字体路径
        for font_path in font_paths:
            if os.path.exists(font_path):
                matplotlib.font_manager.fontManager.addfont(font_path)
                font_name = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams['font.sans-serif'] = [font_name] + matplotlib.rcParams['font.sans-serif']
                print(f"✅ 添加中文字体: {font_name}")
                break
        
        # 设置其他相关参数
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        print("✅ 中文字体配置完成")
        
    except Exception as e:
        print(f"⚠️  中文字体配置失败: {e}")
        print("📝 将使用默认字体，中文可能显示为方框")

# 初始化中文字体
setup_chinese_font()

# 尝试导入数据源库
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    print("提示: tushare未安装，使用模拟数据演示")
    print("安装命令: pip install tushare")
    TUSHARE_AVAILABLE = False
    ts = None

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    print("提示: yfinance未安装，使用模拟数据演示")
    print("安装命令: pip install yfinance")
    YFINANCE_AVAILABLE = False
    yf = None

class BankStockAnalyzer:
    """银行股分析器"""
    
    def __init__(self, use_real_data=True):
        """
        初始化分析器
        
        参数:
            use_real_data: 是否使用真实数据（需要安装tushare/yfinance）
        """
        self.use_real_data = use_real_data
        
        # A股主要银行股列表（股票代码和名称）
        self.bank_stocks = {
            '600036.SS': '招商银行',
            '601398.SS': '工商银行', 
            '601939.SS': '建设银行',
            '601288.SS': '农业银行',
            '601988.SS': '中国银行',
            '601328.SS': '交通银行',
            '600000.SS': '浦发银行',
            '601166.SS': '兴业银行',
            '600016.SS': '民生银行',
            '600919.SS': '江苏银行'
        }
        
        # 模拟数据（用于演示）
        self.mock_dividend_data = self._create_mock_data()
        
    def _create_mock_data(self):
        """创建模拟数据用于演示"""
        years = ['2020', '2021', '2022', '2023', '2024']
        
        # 模拟分红数据（单位：元/股）
        mock_data = {}
        for code, name in self.bank_stocks.items():
            base_div = {
                '600036.SS': 1.20,  # 招行分红较高
                '601398.SS': 0.30,
                '601939.SS': 0.36,
                '601288.SS': 0.22,
                '601988.SS': 0.23,
                '601328.SS': 0.32,
                '600000.SS': 0.35,
                '601166.SS': 1.20,
                '600016.SS': 0.25,
                '600919.SS': 0.40
            }.get(code, 0.30)
            
            # 每年小幅增长
            dividends = []
            for i, year in enumerate(years):
                growth = 1 + i * 0.03  # 每年增长3%
                div = base_div * growth + np.random.normal(0, 0.02)
                dividends.append(max(0.1, div))  # 确保非负
                
            mock_data[code] = {
                'name': name,
                'dividends': dict(zip(years, dividends)),
                'stock_price': np.random.uniform(5, 40),  # 模拟股价
                'eps': np.random.uniform(0.5, 3.5),  # 每股收益
            }
            
        return mock_data
    
    def fetch_real_data(self, stock_code, years=5):
        """
        获取真实股票数据
        
        参数:
            stock_code: 股票代码（如 '600036.SS'）
            years: 获取多少年的数据
            
        返回:
            包含分红、股价等数据的字典
        """
        if not self.use_real_data:
            print(f"使用模拟数据（如需真实数据请设置use_real_data=True并安装tushare）")
            return self.mock_dividend_data.get(stock_code)
            
        data = {}
        try:
            # 方法1: 使用yfinance（国际数据源）
            if YFINANCE_AVAILABLE and '.SS' in stock_code:
                ticker = yf.Ticker(stock_code)
                
                # 获取分红历史
                dividends = ticker.dividends
                if not dividends.empty:
                    # 获取最近几年的分红
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=years*365)
                    recent_divs = dividends[start_date:end_date]
                    
                    # 按年汇总
                    yearly_divs = recent_divs.resample('Y').sum()
                    data['dividends'] = {
                        str(year.year): round(div, 3)
                        for year, div in yearly_divs.items()
                        if div > 0
                    }
                
                # 获取股价信息
                hist = ticker.history(period="1mo")
                if not hist.empty:
                    data['stock_price'] = hist['Close'].iloc[-1]
                    
            # 方法2: 使用tushare（A股数据源）
            elif TUSHARE_AVAILABLE and ts is not None:
                # 需要先设置tushare token
                # ts.set_token('your_token_here')
                pro = ts.pro_api()
                
                # 获取分红数据（示例）
                # dividend_df = pro.dividend(ts_code=stock_code.replace('.SS', ''))
                # ... 实际代码需要根据tushare API调整
                
                print(f"tushare API需要配置token，此处返回模拟数据")
                return self.mock_dividend_data.get(stock_code)
                
        except Exception as e:
            print(f"获取真实数据失败: {e}")
            print("使用模拟数据继续演示")
            return self.mock_dividend_data.get(stock_code)
            
        return data if data else self.mock_dividend_data.get(stock_code)
    
    def calculate_metrics(self, stock_data):
        """
        计算关键指标
        
        参数:
            stock_data: 股票数据字典
            
        返回:
            包含各项指标的字典
        """
        if not stock_data:
            return {}
            
        metrics = {}
        
        # 基本信息
        metrics['name'] = stock_data.get('name', '未知')
        
        # 当前股价
        price = stock_data.get('stock_price', 0)
        metrics['current_price'] = price
        
        # 分红数据
        dividends = stock_data.get('dividends', {})
        if dividends:
            # 最近一年的分红
            years = sorted(dividends.keys(), reverse=True)
            if years:
                latest_year = years[0]
                latest_div = dividends[latest_year]
                metrics['latest_dividend'] = latest_div
                metrics['latest_year'] = latest_year
                
                # 平均分红
                div_values = list(dividends.values())
                metrics['avg_dividend'] = np.mean(div_values)
                
                # 分红增长率（如果有至少2年数据）
                if len(div_values) >= 2:
                    growth = (div_values[0] - div_values[1]) / div_values[1] * 100
                    metrics['dividend_growth_rate'] = round(growth, 2)
                
                # 股息率（分红/股价）
                if price > 0:
                    metrics['dividend_yield'] = round(latest_div / price * 100, 2)
        
        # 每股收益（如果提供）
        eps = stock_data.get('eps')
        if eps:
            metrics['eps'] = eps
            
            # 分红率（分红/EPS）
            if eps > 0 and 'latest_dividend' in metrics:
                metrics['payout_ratio'] = round(metrics['latest_dividend'] / eps * 100, 2)
        
        return metrics
    
    def analyze_all_banks(self):
        """
        分析所有银行股
        
        返回:
            DataFrame包含所有银行的关键指标
        """
        results = []
        
        for code, name in self.bank_stocks.items():
            print(f"正在分析 {name} ({code})...")
            
            # 获取数据
            stock_data = self.fetch_real_data(code)
            
            # 计算指标
            metrics = self.calculate_metrics(stock_data)
            
            if metrics:
                metrics['code'] = code
                results.append(metrics)
        
        # 转换为DataFrame
        df = pd.DataFrame(results)
        
        # 按股息率排序
        if 'dividend_yield' in df.columns:
            df = df.sort_values('dividend_yield', ascending=False)
            
        return df
    
    def visualize_results(self, df, save_path='bank_analysis_results.png'):
        """
        可视化分析结果
        
        参数:
            df: 包含分析结果的DataFrame
            save_path: 图片保存路径
        """
        if df.empty:
            print("没有数据可可视化")
            return
            
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('A股银行股分红分析', fontsize=16, fontweight='bold')
        
        # 1. 股息率排名
        if 'dividend_yield' in df.columns:
            ax1 = axes[0, 0]
            bars = ax1.barh(df['name'], df['dividend_yield'])
            ax1.set_xlabel('股息率 (%)')
            ax1.set_title('股息率排名')
            ax1.invert_yaxis()  # 最高的在上方
            
            # 在条状图上显示数值
            for bar in bars:
                width = bar.get_width()
                ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                        '{:.2f}%'.format(width), ha='left', va='center')
        
        # 2. 最新分红金额
        if 'latest_dividend' in df.columns:
            ax2 = axes[0, 1]
            df_sorted = df.sort_values('latest_dividend', ascending=False)
            bars2 = ax2.bar(df_sorted['name'], df_sorted['latest_dividend'])
            ax2.set_ylabel('每股分红（元）')
            ax2.set_title('最新年度分红金额')
            ax2.tick_params(axis='x', rotation=45)
            
            # 在条状图上显示数值
            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2, height + 0.01,
                        '{:.2f}'.format(height), ha='center', va='bottom')
        
        # 3. 分红增长率（如果有数据）
        if 'dividend_growth_rate' in df.columns:
            ax3 = axes[1, 0]
            df_growth = df[df['dividend_growth_rate'].notna()].copy()
            if not df_growth.empty:
                df_growth = df_growth.sort_values('dividend_growth_rate', ascending=False)
                colors = ['green' if x > 0 else 'red' for x in df_growth['dividend_growth_rate']]
                bars3 = ax3.bar(df_growth['name'], df_growth['dividend_growth_rate'], color=colors)
                ax3.set_ylabel('增长率 (%)')
                ax3.set_title('分红增长率')
                ax3.tick_params(axis='x', rotation=45)
                ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        # 4. 股价与股息率散点图
        if all(col in df.columns for col in ['current_price', 'dividend_yield']):
            ax4 = axes[1, 1]
            scatter = ax4.scatter(df['current_price'], df['dividend_yield'], s=100, alpha=0.6)
            ax4.set_xlabel('股价（元）')
            ax4.set_ylabel('股息率 (%)')
            ax4.set_title('股价 vs 股息率')
            ax4.grid(True, alpha=0.3)
            
            # 添加股票名称标签
            for idx, row in df.iterrows():
                ax4.annotate(row['name'][:2],  # 只显示前2个字
                           (row['current_price'], row['dividend_yield']),
                           fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"分析图表已保存至: {save_path}")
        plt.show()
        
    def generate_report(self, df, output_file='bank_analysis_report.md'):
        """
        生成分析报告
        
        参数:
            df: 分析结果DataFrame
            output_file: 输出文件路径
        """
        report = []
        report.append("# 银行股分红分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("## 核心发现")
        report.append("")
        
        # 最高股息率
        if 'dividend_yield' in df.columns and not df.empty:
            top_yield = df.iloc[0]
            report.append("1. **最高股息率**: {} ({:.2f}%)".format(top_yield['name'], top_yield['dividend_yield']))
        
        # 最高分红金额
        if 'latest_dividend' in df.columns and not df.empty:
            top_div = df.loc[df['latest_dividend'].idxmax()]
            report.append("2. **最高每股分红**: {} ({:.2f}元)".format(top_div['name'], top_div['latest_dividend']))
        
        # 最有增长潜力
        if 'dividend_growth_rate' in df.columns and not df.empty:
            df_growth = df[df['dividend_growth_rate'].notna()]
            if not df_growth.empty:
                top_growth = df_growth.loc[df_growth['dividend_growth_rate'].idxmax()]
                report.append("3. **最高分红增长率**: {} ({:.2f}%)".format(top_growth['name'], top_growth['dividend_growth_rate']))
        
        report.append("")
        report.append("## 详细数据")
        report.append("")
        
        # 创建Markdown表格
        if not df.empty:
            # 选择要显示的列
            display_cols = ['name', 'code', 'current_price', 'latest_dividend', 
                          'dividend_yield']
            if 'dividend_growth_rate' in df.columns:
                display_cols.append('dividend_growth_rate')
            if 'payout_ratio' in df.columns:
                display_cols.append('payout_ratio')
                
            display_df = df[display_cols].copy()
            
            # 重命名列名
            col_names = {
                'name': '银行名称',
                'code': '股票代码',
                'current_price': '当前股价',
                'latest_dividend': '最新分红',
                'dividend_yield': '股息率(%)',
                'dividend_growth_rate': '分红增长率(%)',
                'payout_ratio': '分红率(%)'
            }
            display_df = display_df.rename(columns=col_names)
            
            # 转换为Markdown表格
            report.append(display_df.to_markdown(index=False))
        
        report.append("")
        report.append("## 投资建议")
        report.append("")
        report.append("1. **追求高股息**: 关注股息率排名靠前的银行股")
        report.append("2. **注重稳定性**: 分红连续增长的银行更具投资价值")
        report.append("3. **平衡增长**: 考虑股息率和分红增长率的平衡")
        report.append("4. **风险提示**: 银行股受宏观经济和政策影响较大")
        
        report.append("")
        report.append("---")
        report.append("*本报告由程序员的价投之路公众号提供的Python脚本生成*")
        report.append("*数据仅供参考，不构成投资建议*")
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
            
        print("分析报告已保存至: {}".format(output_file))


def main():
    """主函数：演示完整分析流程"""
    print("=" * 60)
    print("银行股分红分析脚本")
    print("公众号：程序员的价投之路")
    print("=" * 60)
    
    # 创建分析器（使用真实数据需要设置use_real_data=True并安装相应库）
    analyzer = BankStockAnalyzer(use_real_data=False)
    
    print("\n1. 分析所有银行股...")
    results_df = analyzer.analyze_all_banks()
    
    if not results_df.empty:
        print("\n2. 分析结果摘要:")
        print(results_df[['name', 'code', 'current_price', 'latest_dividend', 'dividend_yield']].head())
        
        print("\n3. 生成可视化图表...")
        analyzer.visualize_results(results_df)
        
        print("\n4. 生成分析报告...")
        analyzer.generate_report(results_df)
        
        print("\n5. 分析完成！")
        print("生成的输出文件:")
        print("  - bank_analysis_results.png (分析图表)")
        print("  - bank_analysis_report.md (分析报告)")
        
        print("\n6. 单只股票深度分析示例（招商银行）...")
        cmb_data = analyzer.fetch_real_data('600036.SS')
        cmb_metrics = analyzer.calculate_metrics(cmb_data)
        
        print("\n招商银行关键指标:")
        for key, value in cmb_metrics.items():
            if key not in ['name', 'code']:
                print("  {}: {}".format(key, value))
    else:
        print("分析失败，未获取到数据")


if __name__ == "__main__":
    main()