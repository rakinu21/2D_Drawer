class ShapeDeleter:
    def __init__(self, canvas):
        self.canvas = canvas

    def delete_last_shape(self, event):
        # Find the last drawn shape on the canvas
        last_shape = self.canvas.find_all()[-1] if self.canvas.find_all() else None
        if last_shape:
            # Delete the last drawn shape
            self.canvas.delete(last_shape)
            # Find and destroy the corresponding label
            label_id = f"label{last_shape}"
            label = self.canvas.find_withtag(label_id)
            if label:
                self.canvas.delete(label)