function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function bookmark_this_page() {
    const url = encodeURIComponent(location.href.replace(location.origin, ''))
    const title = encodeURIComponent(document.title.split(' — ')[0])
    window.location.assign(`/?i=App.Client.Bookmark&title=${title}&url=${url}`)
}
