
def reset(layoutAsk, layoutAnswer):
     
    layoutAnswer.configure(state="normal")
    layoutAnswer.delete("1.0", "end")
    layoutAsk.delete("1.0", "end")
    layoutAnswer.configure(state="disabled")