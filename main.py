from fastmcp import FastMCP 
import random 
import json 

mcp=FastMCP("Simple Calculator Server") 


@mcp.tool
def add(a:int,b:int):
    """
    Adds two numbers together.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.
    """
    return a+b

@mcp.tool 
def random_number(min_val:int=1,max_val:int=100):
    """
    Generate a random number within the range.

    Args:
        min_val: Minimum value (default:1)
        max_val: Maximum value (default:100)
    Returns: 
        A random integer between min_val and max_val 
    """
    return random.randint(min_val,max_val)



mcp.resource("info://server")
def server_info()->str:
    """
    Get information about the server.
    """
    info={
          'name':"Simple Calculator Server",
          "version":"1.0.0",
          "description":"A simple calculator server",
          'tools':["add","random_number"],
          "authors":["Charul Chim"]
    }
    return json.dumps(info,indent=2)



if __name__=="__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)







