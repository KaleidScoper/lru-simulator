document.getElementById("lru-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const length = parseInt(document.getElementById("length").value);
    const maxPage = parseInt(document.getElementById("max-page").value);
    const frameCount = parseInt(document.getElementById("frame-count").value);

    // 随机生成页面访问序列
    const pages = Array.from({ length }, () => Math.floor(Math.random() * maxPage) + 1);

    // 运行 LRU 算法
    const { pageFaults, replacementHistory, stackStates } = lruPageReplacement(pages, frameCount);

    // 显示结果
    const results = document.getElementById("results");
    results.textContent = `页面访问序列: ${pages.join(", ")}\n\n`;
    results.textContent += `内存页框大小: ${frameCount}\n\n`;
    results.textContent += "置换图:\n";
    replacementHistory.forEach(({ page, replaced }, index) => {
        results.textContent += `访问页面 ${page} -> ${replaced ? `替换页面 ${replaced}` : "无替换"}\n`;
    });
    results.textContent += "\n栈的变化:\n";
    stackStates.forEach((state, index) => {
        results.textContent += `访问页面 ${pages[index]} 后栈状态: [${state.join(", ")}]\n`;
    });
    results.textContent += `\n总页面错误数: ${pageFaults}`;
});

function lruPageReplacement(pages, frameCount) {
    const frames = [];
    let pageFaults = 0;
    const replacementHistory = [];
    const stackStates = [];

    pages.forEach(page => {
        if (!frames.includes(page)) {
            pageFaults++;
            const replaced = frames.length === frameCount ? frames.shift() : null;
            frames.push(page);
            replacementHistory.push({ page, replaced });
        } else {
            // 页面命中，更新为最近使用
            frames.splice(frames.indexOf(page), 1);
            frames.push(page);
            replacementHistory.push({ page, replaced: null });
        }
        stackStates.push([...frames]);
    });

    return { pageFaults, replacementHistory, stackStates };
}
