import re

def extract_bullet_points(text):
    lines = text.splitlines()
    bullets = []
    current_bullet = ""

    for line in lines:
        if re.match(r'^\s*-\s+', line):  # Check if line starts with '- '
            if current_bullet:
                bullets.append(current_bullet.strip())  # Save the previous bullet
            current_bullet = re.sub(r'^\s*-\s+', '', line)  # Start new bullet
        elif current_bullet and not re.match(r'^\s*\w.+\|', line) and not re.match(r'^\s*(Skills|Projects|Experience)', line, re.IGNORECASE):
            # If it's part of a bullet AND NOT a job title, project name, or skills section
            current_bullet += " " + line.strip()
        else:
            if current_bullet:
                bullets.append(current_bullet.strip())
            current_bullet = ""  # Reset if it's a job title or new section

    if current_bullet:
        bullets.append(current_bullet.strip())

    return bullets

def extract_numbers(bullets):
    bullet_numbers = []
    for bullet in bullets:
        # Find numbers, including:
        # - integers (e.g. 15, 8000)
        # - decimals (e.g. 1.4)
        # - percentages (e.g. 60%)
        # - negative numbers (e.g. -12%)
        numbers = re.findall(r'-?\d+\.?\d*%?', bullet)

        for number in numbers:
            bullet_numbers.append(number)
    return bullet_numbers

def get_quant_metrics_score(raw_resume):
    bullets = extract_bullet_points(raw_resume)
    numbers = extract_numbers(bullets)

    return f"{round((len(numbers) / len(bullets))*100, 2)}%"

