async function show_notify(content, time=8000) {
    // 获取模板
    let temp = document.querySelector("#notification-temp").innerHTML
    // 编译模板
    let template = ejs.compile(temp)
    let html_output = template({ content })
    let place_holder = document.createElement("div")
    place_holder.innerHTML = html_output

    // 添加类
    let child = place_holder.children[0]
    document.querySelector("#notification").appendChild(child)
    child.classList.add("toast-active")
    // 定时 8 秒后关闭
    setTimeout(() => {
        close_notify(child.children[0].children[1])
    }, time)
}
async function close_notify(obj) {
    // 查找并获取父元素
    let parent = obj.parentElement.parentElement
    // 移除类，隐藏元素
    parent.classList.remove("toast-active")
    setTimeout(() => {
        // 移除元素
        parent.remove()
    }, 400)
}
