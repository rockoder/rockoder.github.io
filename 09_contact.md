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
<div id="social-list">
	<div class="social">
		<a target="_blank"  href="https://github.com/rockoder"><img border="0" src="{{ site.url }}/public/images/icons/github.png" ></a>
    </div>
	<div class="social">
		<a target="_blank"  href="https://twitter.com/rockoder"><img border="0" src="{{ site.url }}/public/images/icons/twitter.png" ></a>
    </div>
	<div class="social">
		<a target="_blank"  href="http://stackoverflow.com/users/62849/rockoder"><img border="0" src="{{ site.url }}/public/images/icons/stackoverflow.png" ></a>
    </div>
	<div class="social">
		<a target="_blank"  href="http://www.linkedin.com/in/rockoder"><img border="0" src="{{ site.url }}/public/images/icons/linkedin.png" ></a>
    </div>
</div>

---

You can also drop me a quick message using below form. The form submission will go through [formspree.io](https://formspree.io). I respect your privacy.

<label style="color:blue" id="ackText">Message successfully submitted. Thank you for your message.</label>
<script>getParameterByName('ackText');</script>

<form method="POST" action="http://formspree.io/ganesh@rockoder.com">
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
	#social-list {
	position: relative;
	overflow: hidden;
	}
	.social {
		position: relative;
	    float: left;
	    margin-right: 20px;
	}

.form-style-1 {
    max-width: 400px;
    padding: 0px 12px 10px 0px;
    font: 20px "PT Sans", Helvetica, Arial, sans-serif;
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
.form-style-1 input[type=text],
.form-style-1 input[type=date],
.form-style-1 input[type=datetime],
.form-style-1 input[type=number],
.form-style-1 input[type=search],
.form-style-1 input[type=time],
.form-style-1 input[type=url],
.form-style-1 input[type=email],
textarea,
select{
    box-sizing: border-box;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    border:1px solid #BEBEBE;
    padding: 7px;
    margin:0px;
    -webkit-transition: all 0.30s ease-in-out;
    -moz-transition: all 0.30s ease-in-out;
    -ms-transition: all 0.30s ease-in-out;
    -o-transition: all 0.30s ease-in-out;
    outline: none; 
}
.form-style-1 input[type=text]:focus,
.form-style-1 input[type=date]:focus,
.form-style-1 input[type=datetime]:focus,
.form-style-1 input[type=number]:focus,
.form-style-1 input[type=search]:focus,
.form-style-1 input[type=time]:focus,
.form-style-1 input[type=url]:focus,
.form-style-1 input[type=email]:focus,
.form-style-1 textarea:focus,
.form-style-1 select:focus{
    -moz-box-shadow: 0 0 8px #BCBCBC;
    -webkit-box-shadow: 0 0 8px #BCBCBC;
    box-shadow: 0 0 8px #BCBCBC;
    border: 1px solid #BCBCBC;
}
.form-style-1 .field-divided{
    width: 49%;
}

.form-style-1 .field-long{
    width: 100%;
}
.form-style-1 .field-select{
    width: 100%;
}
.form-style-1 .field-textarea{
    height: 100px;
}
.form-style-1 input[type=submit], .form-style-1 input[type=button]{
    background: #202020;
    padding: 8px 15px 8px 15px;
    border: none;
    color: #fff;
    font: 20px "PT Sans", Helvetica, Arial, sans-serif;
}
.form-style-1 input[type=submit]:hover, .form-style-1 input[type=button]:hover{
    background: #030303;
    box-shadow:none;
    -moz-box-shadow:none;
    -webkit-box-shadow:none;
    font: 20px "PT Sans", Helvetica, Arial, sans-serif;
}
.form-style-1 .required{
    color:red;
}
</style>