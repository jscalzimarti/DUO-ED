username_conditions="""
<div id="error-message">
    <pre>
        Username must contain: 
            8-20 characters
            Must not contain spaces
    </pre>       
</div>
"""

invalid_username_conditions="""
<div id="error-message" style="color: red;">
    <pre>
        Username must contain: 
            8-20 characters
            Must not contain spaces
    </pre>       
</div>
"""

password_conditions="""
<div id="error-message">
    <pre>
        Password must contain:
            8-20 characters
            1 lower case letter: [a-z]
            1 upper case letter: [A-Z]
            1 numeric character: [0-9]
            1 special character: ~`!@#$%^&*()-_+=}{[]|\;:
    </pre>    
</div>
"""

invalid_password_conditions="""
<div id="error-message" style="color: red;">
    <pre>
        Password must contain:
            8-20 characters
            1 lower case letter: [a-z]
            1 upper case letter: [A-Z]
            1 numeric character: [0-9]
            1 special character: ~`!@#$%^&*()-_+=}{[]|\;:
    </pre>    
</div>
"""