---
layout: page
title: Contact
permalink: /contact/
---

<script type="text/javascript">
	function getParameterByName(name) {
    	document.getElementById(name).style.visibility = "hidden";

	    url = window.location.href;

	    name = name.replace(/[\[\]]/g, "\\$&");
	    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
	    results = regex.exec(url);
	    
	    if (!results) return null;
	    
	    if (!results[2]) return '';

	    document.getElementById(name).style.visibility = "visible";

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

<label style="color:blue" id="ackText">Message successfully submitted. Thank you for your message.</label>
<script>getParameterByName('ackText');</script>

<form method="POST" action="https://formspree.io/ganesh@rockoder.com">
<ul class="form-style-1">
    <li>
        <label>Email <span class="required">*</span></label>
        <input type="email" name="email" class="field-long" />
        <input type="hidden" name="_next" value="//{{ site.url }}/contact?ackText=1" />
    </li>
    <li>
        <label>Your Message <span class="required">*</span></label>
        <textarea name="message" id="message" class="field-long field-textarea"></textarea>
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
}

.form-style-1 .field-textarea{
    height: 100px;
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
.form-style-1 .required{
    color:red;
}
</style>
