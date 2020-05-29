<body>
<!-- -->

<h2>Boilerplate for Python + Pytest + requests + Allure API automation test project</h2>

<div>
<ul>
	<li>Created some tests</li>
	<li>Created tests configuration</li>
	<li>Enabled allure reporter</li>
	<li>Added logging</li>
</ul>
</div>

<div>
<h3>To integrate PyCharm with PyTest</h3>
<p>Preferences -> Tools -> Default test runner -> pytest</p>
</div>

<div>
<h3>How to start?</h3>
<ul>
	<li>Create .env file in root directory</li>
	<li>Copy content form .env.example to .env file</li>
	<li>Add to .env deployed Sock Shop IP-address</li>
	<li>Add to .env absolute path to src directory</li>
</ul>
</div>

<div>
<h3>To run marked tests </h3>
<p>For example: you have tests @pytest.mark.api that execute them you need to:<br>
pytest -m api</p>
<p>If you wants to execute test with more then one tag:<br>
pytest -m positive, negative </p>
</div>

<div>
<h3>To run tests with allure report</h3>
<p>chmod +x run.sh<p>
<p>sh run.sh<p>
</div>
</body>