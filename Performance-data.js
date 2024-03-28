// 使用动态导入以兼容 CommonJS
(async () => {
  const lighthouse = await import('lighthouse');
  const chromeLauncher = await import('chrome-launcher');

  async function runLighthouse(url) {
    const chrome = await chromeLauncher.launch({chromeFlags: ['--headless']});
    const options = {logLevel: 'info', output: 'json', onlyCategories: ['performance'], port: chrome.port};
    const runnerResult = await lighthouse.default(url, options);

    // 从 Lighthouse 报告中提取 Time to Interactive (TTI) 和 Total Byte Weight
    const audits = runnerResult.lhr.audits;
    const metrics = {
      timeToInteractive: audits['interactive'].displayValue,
      totalByteWeight: audits['total-byte-weight'].displayValue
    };

    await chrome.kill();
    return metrics;
  }

  // Replace it with the URL you want to test
  const url = 'http://127.0.0.1:5000/book/list';
  runLighthouse(url).then(metrics => {
    console.log(`Metrics for ${url}:`, metrics);
  }).catch(err => {
    console.error('Lighthouse run failed:', err);
  });
})();
