"use strict";


const TRIGGERDIV = document.getElementById("trigger");
const TEMPLATE = document.getElementById("blog-post");
const BLOGLIST = document.getElementById("blog-list");

let counter = 1;


const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        retriveposts();
        counter++;
      }
    });
  });


observer.observe(TRIGGERDIV);


function retriveposts() {
    fetch(`/blog/get?pagenumber=${counter}`)
    .then(response => response.json())
    .then(jsonresponse => {
      if (jsonresponse.length === 0) {
        observer.unobserve(TriggerDiv);
      }
      return jsonresponse;
    })
    .then(data => data.forEach(profile => postblogdom(profile)));
}

function postblogdom (profile) {
    const TemplateClone = TEMPLATE.content.cloneNode(true);

    if (profile.did_like === 'like') TemplateClone.getElementById('blog-like').classList.add('border-2', 'border-black');
    if (profile.did_like === 'dislike') TemplateClone.getElementById('blog-dislike').classList.add('border-2', 'border-black');

    TemplateClone.getElementById('blog-dislike').setAttribute('value', profile.id);
    TemplateClone.getElementById('blog-like').setAttribute('value', profile.id);

    TemplateClone.getElementById('blog-title').textContent = profile.post_title;
    TemplateClone.getElementById('blog-text').textContent = profile.post_text;
    TemplateClone.getElementById('blog-dislike').textContent = profile.dislikes;
    TemplateClone.getElementById('blog-like').textContent = profile.likes;
    TemplateClone.getElementById('blog-author').textContent = profile.post_creator;
    TemplateClone.getElementById('blog-date').textContent = profile.post_date;

    BLOGLIST.appendChild(TemplateClone);
}




// user liked/disliked a blogpost
function bloglike(this_element) {
  const second_button = getsecondSibling(this_element);
  const blog_id = this_element.value;
  const like = this_element.name;


  // if button isnt already selected, add classes and +1
  if(!this_element.classList.contains('border-2')) {
    fetch(`/blog/like/${blog_id}/${like}`)

    let buttonNumber = this_element.textContent;
    this_element.textContent = parseInt(buttonNumber) + 1;
    this_element.classList.add('border-2', 'border-black');
  }

  // retract your like/dislike
  else {
    fetch(`/blog/like/${blog_id}/delete`);
    this_element.classList.remove('border-2', 'border-black');
    this_element.textContent = parseInt(this_element.textContent) - 1;    
  }
  
  // if other element was selected before remove classes and number -1
  if(second_button.classList.contains('border-2')) {
    second_button.classList.remove('border-2', 'border-black');
    second_button.textContent = parseInt(second_button.textContent) - 1;
  }
}


// get the other sibling in th element
function getsecondSibling(sibling_one) {
  const parent_element = sibling_one.parentNode;
  const first_child = parent_element.children[0];
  const second_child = parent_element.children[1];

  if (sibling_one === first_child) return second_child;
  else return first_child
}