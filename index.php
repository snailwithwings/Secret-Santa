<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Secret Santa 2025</title>
<style>
    body {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        background-color: #fbeed8;
        text-align: center;
        padding: 50px;
        color: #5a2a27;
    }
    h1 {
        font-size: 3em;
        color: #d62828;
    }
    h2 {
        font-size: 2em;
        color: #f77f00;
    }
    .gift-box {
        margin: 40px auto;
        width: 200px;
        height: 200px;
        background-color: #ffafcc;
        border: 5px solid #d62828;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5em;
        font-weight: bold;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        cursor: pointer;
        transition: transform 0.2s;
    }
    .gift-box:hover {
        transform: scale(1.1);
    }
    p {
        font-size: 1.2em;
        margin-top: 30px;
    }
</style>
</head>
<body>

<h1>🎅 Secret Santa 2025 🎁</h1>
<h2>Shhh... It's a Secret!</h2>

<div class="gift-box" id="startBox">Your Gift Awaits!</div>

<p>Get ready Movie night!<br>
Please click the box to get started</p>

<script>
    const box = document.getElementById('startBox');
    box.addEventListener('click', () => {
        // Navigate to the second page
        window.location.href = "secret-santa-reveal.html";
    });
</script>

</body>
</html>
