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

async function call(args = {}) {
    const formdata = new FormData()
    Object.entries(args).forEach(item => {
      formdata.append(item[0], item[1])
    })
    return fetch('/api', {
      'method': 'POST',
      'body': formdata
    })
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    e.preventDefault();
  
    if (e.target.tagName == 'TEXTAREA') {
      const textarea = e.target
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;

      textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);

      textarea.selectionStart = textarea.selectionEnd = start + 4;
    }
  }
});
