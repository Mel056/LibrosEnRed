function renderComments(comments) {
    const commentsContainer = document.getElementById('comments');

    if (comments.length === 0) {
        commentsContainer.innerHTML = '<p>No hay comentarios aún.</p>';
        return;
    }

    const commentsHTML = comments.map(comment => `
        <div class="comment">
            <img src="${comment.commenter_photo || '/static/images/default-avatar.jpg'}"
                 alt="${comment.commenter_username}" class="commenter-photo">
            <div class="comment-content">
                <h4>${comment.commenter_username}</h4>
                <p>${comment.comment}</p>
                <small>${new Date(comment.created_at).toLocaleString()}</small>
            </div>
        </div>
    `).join('');

    commentsContainer.innerHTML = commentsHTML;
}