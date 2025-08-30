from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
import pymysql
ap=FastAPI()
@ap.get("/",response_class=HTMLResponse)
def hi():
    return f'''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add New Recipe</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        header {{
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .form-container {{
            padding: 30px;
        }}

        .form-group {{
            margin-bottom: 25px;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #444;
        }}

        .form-control {{
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }}

        .form-control:focus {{
            outline: none;
            border-color: #ff7e5f;
            box-shadow: 0 0 0 3px rgba(255, 126, 95, 0.2);
        }}

        textarea.form-control {{
            min-height: 100px;
            resize: vertical;
        }}

        .ingredients-container {{
            margin-bottom: 15px;
        }}

        .ingredient-input {{
            display: flex;
            margin-bottom: 10px;
        }}

        .ingredient-input input {{
            flex-grow: 1;
            margin-right: 10px;
        }}

        .btn {{
            display: inline-block;
            padding: 12px 25px;
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .btn:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
        }}

        .btn-secondary {{
            background: #6c757d;
        }}

        .btn-danger {{
            background: #dc3545;
            padding: 8px 15px;
        }}

        .form-actions {{
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }}

        .recipe-image-preview {{
            width: 100%;
            max-height: 200px;
            object-fit: cover;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }}

        .difficulty-selector {{
            display: flex;
            gap: 15px;
        }}

        .difficulty-option {{
            flex: 1;
            text-align: center;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .difficulty-option.selected {{
            border-color: #ff7e5f;
            background-color: rgba(255, 126, 95, 0.1);
        }}

        .difficulty-option input {{
            display: none;
        }}

        @media (max-width: 600px) {{
            .form-actions {{
                flex-direction: column;
                gap: 15px;
            }}
            
            .btn {{
                width: 100%;
                text-align: center;
            }}
            
            .difficulty-selector {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Share Your Recipe</h1>
            <p>Fill out the form below to add your delicious recipe to our collection</p>
        </header>
        
        <div class="form-container">
            <form id="recipeForm" action="/submit-recipe" method="post">
                <div class="form-group">
                    <label for="recipeTitle">Recipe Title</label>
                    <input type="text" id="recipeTitle" name="title" class="form-control" placeholder="e.g., Chocolate Chip Cookies" required>
                </div>
                
                <div class="form-group">
                    <label for="recipeDescription">Description</label>
                    <textarea id="recipeDescription" name="description" class="form-control" placeholder="Describe your recipe..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>Ingredients</label>
                    <div class="ingredients-container" id="ingredientsContainer">
                        <div class="ingredient-input">
                            <input type="text" name="ingredients[]" class="form-control" placeholder="e.g., 2 cups flour" required>
                            <button type="button" class="btn btn-danger" onclick="removeIngredient(this)">Remove</button>
                        </div>
                    </div>
                    <button type="button" class="btn btn-secondary" onclick="addIngredient()">Add Another Ingredient</button>
                </div>
                
                <div class="form-group">
                    <label for="recipeInstructions">Instructions</label>
                    <textarea id="recipeInstructions" name="instructions" class="form-control" placeholder="Step-by-step instructions..." required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="prepTime">Preparation Time (minutes)</label>
                    <input type="number" id="prepTime" name="prepTime" class="form-control" min="1" required>
                </div>
                
                <div class="form-group">
                    <label for="cookTime">Cooking Time (minutes)</label>
                    <input type="number" id="cookTime" name="cookTime" class="form-control" min="0" required>
                </div>
                
                <div class="form-group">
                    <label>Difficulty Level</label>
                    <div class="difficulty-selector">
                        <label class="difficulty-option" onclick="selectDifficulty(this)">
                            <input type="radio" name="difficulty" value="easy" required> Easy
                        </label>
                        <label class="difficulty-option" onclick="selectDifficulty(this)">
                            <input type="radio" name="difficulty" value="medium"> Medium
                        </label>
                        <label class="difficulty-option" onclick="selectDifficulty(this)">
                            <input type="radio" name="difficulty" value="hard"> Hard
                        </label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="recipeCategory">Category</label>
                    <select id="recipeCategory" name="category" class="form-control" required>
                        <option value="">Select a category</option>
                        <option value="appetizer">Appetizer</option>
                        <option value="main">Main Course</option>
                        <option value="dessert">Dessert</option>
                        <option value="salad">Salad</option>
                        <option value="soup">Soup</option>
                        <option value="beverage">Beverage</option>
                        <option value="breakfast">Breakfast</option>
                        <option value="snack">Snack</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="recipeServings">Servings</label>
                    <input type="number" id="recipeServings" name="servings" class="form-control" min="1" required>
                </div>
                
                <div class="form-actions">
                    <button type="reset" class="btn btn-secondary">Clear Form</button>
                    <button type="submit" class="btn">Submit Recipe</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // Function to add new ingredient input
        function addIngredient() {{
            const container = document.getElementById('ingredientsContainer');
            const div = document.createElement('div');
            div.className = 'ingredient-input';
            div.innerHTML = `
                <input type="text" name="ingredients[]" class="form-control" placeholder="e.g., 2 cups flour" required>
                <button type="button" class="btn btn-danger" onclick="removeIngredient(this)">Remove</button>
            `;
            container.appendChild(div);
        }}
        
        // Function to remove ingredient input
        function removeIngredient(button) {{
            const container = document.getElementById('ingredientsContainer');
            if (container.children.length > 1) {{
                button.parentElement.remove();
            }}
        }}
        
        // Function to handle difficulty selection
        function selectDifficulty(element) {{
            // Remove selected class from all options
            const options = document.querySelectorAll('.difficulty-option');
            options.forEach(opt => opt.classList.remove('selected'));
            
            // Add selected class to clicked option
            element.classList.add('selected');
            
            // Check the radio button
            const radio = element.querySelector('input[type="radio"]');
            radio.checked = true;
        }}
        
        // Function to preview image before upload
        document.getElementById('recipeImage').addEventListener('change', function(e) {{
            const preview = document.getElementById('imagePreview');
            if (this.files && this.files[0]) {{
                const reader = new FileReader();
                
                reader.onload = function(e) {{
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }}
                
                reader.readAsDataURL(this.files[0]);
            }}
        }});
        
        // Form validation
        document.getElementById('recipeForm').addEventListener('submit', function(e) {{
            let isValid = true;
            const inputs = this.querySelectorAll('input[required], textarea[required], select[required]');
            
            inputs.forEach(input => {{
                if (!input.value.trim()) {{
                    isValid = false;
                    input.style.borderColor = 'red';
                }} else {{
                    input.style.borderColor = '#ddd';
                }}
            }});
            
            if (!isValid) {{
                e.preventDefault();
                alert('Please fill in all required fields.');
            }}
        }});
    </script>
</body>
</html>
'''


@ap.post("/submit-recipe", response_class=HTMLResponse)
async def submit_recipe(r: Request):
    fd = await r.form()
    title = fd['title']
    description = fd['description']
    ingredients = fd.getlist('ingredients[]')
    instructions = fd['instructions']
    prepTime = fd['prepTime']
    cookTime = fd['cookTime']
    difficulty = fd['difficulty']
    category = fd['category']
    servings = fd['servings']

    # Convert ingredients list to string for database storage
    ingredients_str = "\n".join(ingredients)

    sql = "INSERT INTO recipes (title, description, ingredients, instructions, prep_time, cook_time, difficulty, category, servings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    vals = (title, description, ingredients_str, instructions, prepTime, cookTime, difficulty, category, servings)

    con = pymysql.connect(host="localhost", user="root", password="yourpassword", database="recipe_app")
    cur = con.cursor()
    cur.execute(sql, vals)
    con.commit()
    con.close()

    return f'''<h2>Recipe "{title}" has been successfully submitted!</h2>
               <p><a href="/">Submit another recipe</a></p>
               <p><a href="/saved">View saved recipes</a></p>'''


@ap.get("/saved", response_class=HTMLResponse)
def view_saved_recipes():
    # Connect to database
    con = pymysql.connect(host="localhost", user="root", password="yourpassword", database="recipe_app")
    cur = con.cursor()

    # Fetch all recipes ordered by title
    cur.execute(
        "SELECT title, description, ingredients, instructions, prep_time, cook_time, difficulty, category, servings FROM recipes ORDER BY title")
    recipes = cur.fetchall()

    con.close()

    # Generate HTML for recipes
    recipes_html = ""
    if recipes:
        for recipe in recipes:
            recipes_html += f"""
            <div class="recipe-card">
                <div class="recipe-content">
                    <h3 class="recipe-title">{recipe[0]}</h3>
                    <p class="recipe-category"><strong>Category:</strong> {recipe[7]}</p>
                    <p class="recipe-difficulty"><strong>Difficulty:</strong> {recipe[6]}</p>
                    <p class="recipe-time"><strong>Prep:</strong> {recipe[4]} min | <strong>Cook:</strong> {recipe[5]} min</p>
                    <p class="recipe-servings"><strong>Servings:</strong> {recipe[8]}</p>
                    <p class="recipe-description">{recipe[1][:150] if recipe[1] else 'No description available'}...</p>
                    <div class="recipe-actions">
                        <button class="btn view-details" onclick="showRecipeDetails(this)">View Details</button>
                        <div class="recipe-full-details" style="display: none;">
                            <h4>Ingredients:</h4>
                            <p>{recipe[2].replace(chr(10), '<br>')}</p>
                            <h4>Instructions:</h4>
                            <p>{recipe[3]}</p>
                        </div>
                    </div>
                </div>
            </div>
            """
    else:
        recipes_html = "<div class='empty-state'><p>No recipes saved yet. <a href='/'>Add your first recipe!</a></p></div>"

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Saved Recipes</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
                padding: 20px;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}

            header {{
                background: linear-gradient(135deg, #ff7e5f, #feb47b);
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 10px 10px 0 0;
                margin-bottom: 20px;
            }}

            header h1 {{
                font-size: 2.2rem;
                margin-bottom: 10px;
            }}

            .back-link {{
                display: inline-block;
                margin-top: 20px;
                color: #ff7e5f;
                text-decoration: none;
                font-weight: 600;
            }}

            .back-link:hover {{
                text-decoration: underline;
            }}

            .recipes-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}

            .recipe-card {{
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }}

            .recipe-card:hover {{
                transform: translateY(-5px);
            }}

            .recipe-title {{
                font-size: 1.4rem;
                color: #333;
                margin-bottom: 10px;
            }}

            .recipe-category, .recipe-difficulty, .recipe-time, .recipe-servings {{
                margin-bottom: 8px;
                color: #666;
            }}

            .recipe-description {{
                color: #777;
                margin: 15px 0;
                line-height: 1.5;
            }}

            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background: linear-gradient(135deg, #ff7e5f, #feb47b);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s;
                margin-top: 10px;
            }}

            .btn:hover {{
                opacity: 0.9;
                transform: translateY(-2px);
            }}

            .empty-state {{
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                grid-column: 1 / -1;
            }}

            .recipe-full-details {{
                margin-top: 15px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 5px;
                border-left: 4px solid #ff7e5f;
            }}

            .recipe-full-details h4 {{
                margin-bottom: 8px;
                color: #333;
            }}

            @media (max-width: 768px) {{
                .recipes-grid {{
                    grid-template-columns: 1fr;
                }}

                header h1 {{
                    font-size: 1.8rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Your Saved Recipes</h1>
                <p>All your delicious creations in one place</p>
            </header>

            <div class="recipes-grid">
                {recipes_html}
            </div>

            <a href="/" class="back-link">← Back to Add Recipe</a>
        </div>

        <script>
            function showRecipeDetails(button) {{
                const detailsDiv = button.nextElementSibling;
                if (detailsDiv.style.display === 'none') {{
                    detailsDiv.style.display = 'block';
                    button.textContent = 'Hide Details';
                }} else {{
                    detailsDiv.style.display = 'none';
                    button.textContent = 'View Details';
                }}
            }}
        </script>
    </body>
    </html>
    '''
