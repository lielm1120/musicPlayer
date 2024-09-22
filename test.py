from bs4 import BeautifulSoup
import re


def generate_meaningful_name(element):
    name_parts = []
    if element.get('name'):
        name_parts.append(element['name'])
    if element.get('id'):
        name_parts.append(element['id'])
    if not name_parts:
        name_parts.append(element.name)
    return "_".join(name_parts)


def generate_java_pom_class(html_content, class_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all(
        lambda tag: tag.name in ['input', 'button', 'a'] and (tag.has_attr('id') or tag.has_attr('name')))
    unique_elements = {el.get('id') or el.get('name'): el for el in elements}
    java_class = f"import org.openqa.selenium.WebDriver;\n"
    java_class += f"import org.openqa.selenium.WebElement;\n"
    java_class += f"import org.openqa.selenium.support.FindBy;\n"
    java_class += f"import org.openqa.selenium.support.PageFactory;\n\n"
    java_class += f"public class {class_name} '{'{'}\n\n"
    java_class += "    // WebDriver definition\n"
    java_class += "    private WebDriver driver;\n\n"
    java_class += f"    public {class_name}(WebDriver driver) {'{'}\n"
    java_class += "        this.driver = driver;\n"
    java_class += "        PageFactory.initElements(driver, this);\n"
    java_class += "    }\n\n"
    java_class += "    //Data members\n\n"

    for identifier, element in unique_elements.items():
        meaningful_name = generate_meaningful_name(element)
        clean_identifier = re.sub(r'\W|^(?=\d)', '_', meaningful_name)

        if element.get("id"):
            locator = f"@FindBy(id = \"{element['id']}\")"
        elif element.get("name"):
            locator = f"@FindBy(name = \"{element['name']}\")"

        java_class += f"    {locator}\n"
        java_class += f"    private WebElement {clean_identifier};\n\n"

    java_class += "    // Methods\n\n"

    for identifier, element in unique_elements.items():
        meaningful_name = generate_meaningful_name(element)
        clean_identifier = re.sub(r'\W|^(?=\d)', '_', meaningful_name)

        element_type = element.name
        if element_type == 'input':
            java_class += f"    public void enter{clean_identifier.capitalize()}(String value) {'{'}\n"
            java_class += f"        {clean_identifier}.clear();\n"
            java_class += f"        {clean_identifier}.sendKeys(value);\n"
            java_class += f"    }}\n\n"
        elif element_type in ['button', 'a']:
            java_class += f"    public void click{clean_identifier.capitalize()}() {'{'}\n"
            java_class += f"        {clean_identifier}.click();\n"
            java_class += f"    }}\n\n"

    java_class += "}\n"
    return java_class


html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <div id="main">
        <input type="text" id="username" name="username"/>
        <input type="password" id="password" name="password"/>
        <button id="loginBtn">Login</button>
        <a href="profile.html" id="profileLink">Profile</a>
    </div>
</body>
</html>
"""

java_class_content = generate_java_pom_class(html_content, "LoginPage")
print(java_class_content)
