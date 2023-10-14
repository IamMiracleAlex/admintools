The New Annotation-Apis module consists of 2 main functions.

## 1. The 'get':

#1.0.0 
This function is responsible for getting a new task i.e every call 
to this function starts a Task. The `mode = request.query_params.get('mode',
 "annotator")` gets the mode from the Chrome Extension. It sets **annotator** 
as default just incase no mode is provided by the Chrome Extension. Mode can 
be either **annotation** or **developer**. We have different Modes so the 
Extension can distinguish the type of data to expect,where and how 
to store them. The **annotation** mode when specified tells the Extension 
to create a Task for the current user while **Developer** mode is 
more like a testing environment. Also, the `annotators_assigned` 
counter is not incremented if it's in developer mode so that the 
url can get assigned to a real annotator. The function stores 
the result in the **mode** variable and it **returns** the 
`get_next_task` by passing the **mode** variable as parameter.


#1.1.0 `get_next_task`:

#1.2.0 
The `get_next_task` fetches a url from annotation queue and creates 
a new task from it or it retrieves an existing incomplete task.

#1.3.0 
The `if existing_task.exists():` checks if the **User** has an existing task;
#1.3.1 
If the user does have an existing Task, the `if existing_task.exists():`  
condition checks **True**. The `task = existing_task.first()` statement fetches 
the First existing incomplete task but clear previously completed steps 
and create a new task for the **User** so the chrome extension can have 
a fresh start.
#1.3.2 
If the user does not have an existing Task, the `if existing_task.exists():`  
condition checks **False**. The function fetches 
a new Url for annotation from the **tbaq(To Be Annotated Queue)**. 
The function create a new Task with the Url returned from the **tbaq**, 
User and Mode as parameters to the **create** function. The function 
checks if the current Mode is **annotators**, if **True** it increment 
the **Url Annotators Assigned Count**. The First Step for this Task is 
being created with the `task.steps.create()` statement and assigned to 
the **step** variable.

#1.4.0 
The `if step:` statement checks the validity of the **step** variable;
#1.4.1 
If a Step has been created for the new Task, the `if step:` condition 
checks **True**, the function **serialize** the data in the **step** 
variable using the `StepSerializer` function. The `StepSerializer` is a 
user-defined function from the **Django REST Framework** which is used 
to convert data to a JSON-like format. 
#1.4.2 
If no Step has been created for the new Task, the `if step:` condition 
checks **False**. The function returns a **HTTP_503_SERVICE_UNAVAILABLE** 
response to the caller saying **No url to annotate at this time**.



## 2. The `post`:

#2.0.0	
The `post` Submits annotation data for each step. A new step is returned 
after each submission or a new task if the last step was submitted. It 
starts by calling the `StepSubmitSerializer` function so as to Serialize 
the data extracted from the current working url page and checks if the 
data is valid. The `post` function then checks the current **step** of 
the serialized data it received. The steps can be either **page_products**, 
**products_entities**, **entities_classification** and **bad_url**.

#2.1.0 
The `if current_step == "bad_url":` statement checks if the current **step** 
is a **bad_urls**.
#2.1.1 
If the current step is **bad_urls**, the `if current_step == "bad_url":` 
condition checks **True**, the function filter out the current working 
url and update it step to **bad_url**.  
#2.1.2 
If the `if current_step == "bad_url":` condition checks **False** i.e the 
**step** is not a **bad_url**, the function updates the **step** to either 
**page_products**, **products_entities**, **entities_classification**, marks 
it as Completed and saves it. Otherwise, it returns a **HTTP_404_NOT_FOUND** 
if the function raises a **Step.DoesNotExist** exception. 


#2.2.0 
The `post` function checks for the next step by calling the `step.next_step` 
statement. 
#2.2.1 
If there is a next step, the `step.next_step` condition checks **True**. 
The function fetches the existing **step** and if there is no existing step, 
it creates a new **step**. The `post` function then serialize the **step** 
data using the **StepSerializer** function and it passes the data with the 
**return** statement using the `Response` function.
#2.2.2 
If no next step exists, the `step.next_step` condition checks **False**. The 
function marks the current **task** as Completed and return a new Task.