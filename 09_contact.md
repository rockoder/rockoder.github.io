---
layout: page
title: Contact
permalink: /contact/
---

<script type="text/javascript">
	function getParameterByName(name) {
	    var url = window.location.href;
	    name = name.replace(/[\[\]]/g, "\\$&");
	    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
	    results = regex.exec(url);
	    
	    if (!results || !results[2]) return null;

	    var element = document.getElementById(name);
	    if (element) {
	        element.style.display = "block";
	    }

	    return '';
	}
</script>

You can reach out to me on:
<div id="social-list1" class="contact-socials">
	<div class="social1">
		<a target="_blank" href="https://twitter.com/rockoder" aria-label="Twitter">{% include icon-twitter.svg %}</a>
    </div>
	<div class="social1">
		<a target="_blank" href="https://github.com/rockoder" aria-label="GitHub">{% include icon-github.svg %}</a>
    </div>
	<div class="social1">
		<a target="_blank" href="https://www.linkedin.com/in/rockoder" aria-label="LinkedIn">{% include icon-linkedin.svg %}</a>
    </div>
</div>

<style>
  .contact-socials {
    justify-content: flex-start !important;
  }
  .contact-socials .social1 svg path {
    fill: var(--link-color) !important;
  }
</style>

---

You can also drop me a quick message using below form. The form submission will go through [formspree.io](https://formspree.io). I respect your privacy.

<div id="ackText" class="status-message success" style="display: none;" role="status" aria-live="polite">
  Message successfully submitted. Thank you for your message.
</div>
<script>getParameterByName('ackText');</script>

<form method="POST" action="https://formspree.io/ganesh@rockoder.com">
<ul class="form-style-1">
    <li>
        <label for="email">Email <span class="required">*</span></label>
        <input type="email" id="email" name="email" class="field-long" required />
        <input type="hidden" name="_next" value="{{ site.url }}/contact?ackText=1" />
    </li>
    <li>
        <label for="message">Your Message <span class="required">*</span></label>
        <textarea name="message" id="message" class="field-long field-textarea" required></textarea>
    </li>
    <li>
        <input type="submit" value="Submit" />
    </li>
</ul>
</form>

---

<style type="text/css">
.form-style-1 {
    max-width: 400px;
    padding: 0px 12px 10px 0px;
}
.form-style-1 li {
    padding: 0;
    display: block;
    list-style: none;
    margin: 10px 0 0 0;
}
.form-style-1 label{
    margin:0 0 3px 0;
    padding:0px;
    display:block;
    font-weight: bold;
}
.form-style-1 input[type=email],
textarea {
    box-sizing: border-box;
    border: 1px solid var(--border-color);
    padding: 10px;
    margin: 0px;
    width: 100%;
    background: var(--body-bg);
    color: var(--body-color);
    border-radius: 4px;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.form-style-1 input[type=email]:focus,
textarea:focus {
    outline: none;
    border-color: var(--link-color);
    box-shadow: 0 0 0 3px rgba(38, 139, 210, 0.2);
}

.form-style-1 .field-textarea{
    height: 100px;
}

.status-message {
    padding: 1rem;
    margin-bottom: 1.5rem;
    border-radius: 4px;
    font-weight: bold;
}

.status-message.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

@media (prefers-color-scheme: dark) {
    .status-message.success {
        background-color: #1c3321;
        color: #8fdfa1;
        border-color: #2b4c33;
    }
}
.form-style-1 input[type=submit] {
    background: var(--sidebar-bg);
    padding: 10px 20px;
    border: none;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
}
.form-style-1 input[type=submit]:hover {
    background: #000;
}
.form-style-1 input[type=submit]:focus-visible {
    outline: 3px solid var(--link-color);
    outline-offset: 2px;
}
.form-style-1 .required{
    color:red;
}
</style>
