document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = Cookies.get('csrftoken');
    const likeButtons = document.querySelectorAll('a.like');
    const url = likeButtons[0].dataset.url;
    

    var options = {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin'
    }

    likeButtons.forEach(function(likeButton) {
    likeButton.addEventListener('click', function (e) {
      e.preventDefault();
      var likeButton = this;
      var formData = new FormData();
      formData.append('id', likeButton.dataset.id);
      formData.append('action', likeButton.dataset.action);
      options['body'] = formData;
      var postId = this.getAttribute('data-id');
      var likeCountElement = document.getElementById(postId);
     
      fetch(url, options, postId)
          .then(response => response.json())
          .then(data => {
              if (data['status'] === 'ok') {
                  var previousAction = likeButton.dataset.action;
                  var action = previousAction === 'like' ? 'unlike' : 'like';
                  likeButton.dataset.action = action;
                  likeButton.innerHTML = action;
                  likeButton.text = (previousAction == 'like' ? '👎' : '👍');
                  

                  var likeCount = likeCountElement.textContent;
                  var totalLikes = parseInt(likeCount);
                  likeCountElement.textContent = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;
              }
          })
          .catch(error => {
              console.error('Fetch error:', error);
          });
    })
  });
  })