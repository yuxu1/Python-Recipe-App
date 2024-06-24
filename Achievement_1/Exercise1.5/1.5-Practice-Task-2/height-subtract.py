class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        output = str(self.feet) + " feet, " + str(self.inches) + " inches"
        return output

    def __sub__(self, other):
        # Converting both objects' heights into inches
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches

        # Subtracting height of B from A
        height_difference_inches = height_A_inches - height_B_inches

        # Getting the output in feet
        output_feet = height_difference_inches // 12

        # Getting the output in inches
        output_inches = height_difference_inches - (output_feet * 12)

        # Returning the final output as a new Height object
        return Height(output_feet, output_inches)

person_A_height = Height(5, 10)
person_B_height = Height(3, 9)
height_difference = person_A_height - person_B_height

print("Height difference:", height_difference)