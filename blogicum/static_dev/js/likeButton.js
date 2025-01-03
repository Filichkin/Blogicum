document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = Cookies.get('csrftoken');
    const url = '{% url "blog:like" %}';
    const likeButtons = document.querySelectorAll('a.like');

    var options = {
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin'
    }

    likeButtons.forEach(function (likeButton) {
    likeButton.addEventListener('click', function (e) {
      e.preventDefault();
      var likeButton = this;
      var formData = new FormData();
      formData.append('id', likeButton.dataset.id);
      formData.append('action', likeButton.dataset.action);
      options['body'] = formData;

      fetch(url, options)
          .then(response => response.json())
          .then(data => {
              if (data['status'] === 'ok') {
                  var previousAction = likeButton.dataset.action;

                  var action = previousAction === 'like' ? 'unlike' : 'like';
                  likeButton.dataset.action = action;
                  likeButton.innerHTML = action;

                  var likeCount = document.querySelector('span.count .total');
                  var totalLikes = parseInt(likeCount.innerHTML);
                  likeCount.innerHTML = previousAction === 'like' ? totalLikes + 1 : totalLikes - 1;

                  location.reload();
              }
          })
          .catch(error => {
              console.error('Fetch error:', error);
          });
    })
  });
  })