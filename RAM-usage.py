from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 配置Chrome选项
chrome_options = Options()
# 如果需要的话，设置Chrome为无头模式
# chrome_options.add_argument("--headless")

# 初始化WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 打开网页
driver.get('http://127.0.0.1:5000/book/list')

# 执行JavaScript代码获取内存使用情况
memory_usage = driver.execute_script("return window.performance.memory")

print(memory_usage)

# 清理，关闭浏览器
driver.quit()
