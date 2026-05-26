from graph import graph

normal_input = {
    "user_id": "u_101",
    "message": "The app crashes when I upload a PDF file."
}

billing_input = {
    "user_id": "u_102",
    "message": "I was charged twice for my subscription."
}

print("Normal technical issue:")
print(graph.invoke(normal_input))

print("\nBilling issue:")
print(graph.invoke(billing_input))





