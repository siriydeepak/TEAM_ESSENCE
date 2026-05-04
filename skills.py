class OpenClawSkill:
    pass

def tool(name=None):
    def decorator(func):
        func.is_tool = True
        func.tool_name = name
        return func
    return decorator
