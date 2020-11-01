"""
 *****************************************************************************
   FILE:        images.py

   DESCRIPTION: Given an picture, write a program to create new picture from 
                the given picture that has features such as blurring picture, 
                picture in inverse color, or picture with color in white, gray, 
                and black only.

 *****************************************************************************
"""
import turtle
import sys     # for giving file name on command line

def neigbor_avg(picture, triple_row, triple_col):
    """ Given location of a pixel, find all possible neighbors
        of that pixel, then find the average value of the numbers
        of the triple between the pixel and its neighbors """

    # Find all posible neighbors of a given pixel triple within
    # the picture
    neigbors_triples = find_neigbor(picture, triple_row, triple_col)

    # Use brute force to add all the values of R, G, B of all
    # triple together respectively
    r_sum = 0
    g_sum = 0
    b_sum = 0
    for triples in neigbors_triples:
        r_sum += triples[0]
        g_sum += triples[1]
        b_sum += triples[2]

    # Find the average values of R, G, B respectively from the
    # the given pixel and its neighbor. And return the average
    # triple of R, G, B.
    avg_R = r_sum // len(neigbors_triples)
    avg_G = g_sum // len(neigbors_triples)
    avg_B = b_sum // len(neigbors_triples)
    return (avg_R, avg_G, avg_B)

def is_in_bounds(picture, possible_row, possible_col):
    """ Return True for each coordinates within the picture.
        Return False otherwise. """
    
    # If (row_loc, col_loc) are smaller than zero or bigger than grid_size, 
    # then (row_loc, col_loc) is outside of grid. Man states len(grid[0]) 
    # will find the number of column of the first row, which is also the 
    # number of column of the whole grid.
    if possible_row < 0 or possible_row >= len(picture):
        return False
    if possible_col < 0 or possible_col >= len(picture[0]):
        return False
    return True

def find_neigbor(picture, p_row, p_col):
    """ Return a list of all possible neigbors. """

    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (0, 0),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]

    # For each direction, check if the given location of a 
    # pixel has neighbor in that direction. If not, change
    # direction.
    neigbors = []
    for dr in directions:
        dr_row = dr[0]
        dr_col = dr[1]

        # Check if neighbor is within the picture
        if is_in_bounds(picture, p_row + dr_row, 
                        p_col + dr_col) is True:
            neigbors.append(picture[p_row + dr_row]
                            [p_col + dr_col])
    return neigbors 

def blur(picture):
    """ Return a new image in which every pixel is the average 
        of itself and its neighbors.(Every pixel has up to 8 
        neighbors.) """

    # Create a new picture in which in pixel has triple of the 
    # average value of the old triple and all of its neigbors
    blurred_picture = []
    for i in range(len(picture)):
        blurred_pixels = []
        for j in range(len(picture[i])):

            # For each location of the pixel, find the all
            # possible neigbor to blur the RGB intensity
            blurred_pixels.append(neigbor_avg(picture, i, j))
        blurred_picture.append(blurred_pixels)
    return blurred_picture

def negative(picture):
    """ Return a new image in which every pixel is the 
        photographic negative of the original pixel. 
        (A dark component becomes a light component, 
        and vice versa). """

    # Cite: Invert a color online - PineTools
    # Source: https://pinetools.com/invert-color
    # Desc: The inverse color can be found by substract 255
    # by the intensity of the given RGB values in the triples

    # Create a new picture in which each pixel had the inverse
    # color triples.
    negative_picture = []
    for i in range(len(picture)):
        inverse_pixels = []
        for j in range(len(picture[i])):
            inverse_pixels.append((255 - picture[i][j][0], 
                                   255 - picture[i][j][1], 
                                   255 - picture[i][j][2]))
        negative_picture.append(inverse_pixels)
    return negative_picture

def grayscale(picture):
    """ Return a new image in which every pixel is a shade of 
        gray equal to the average intensity of the RBG values 
        of each pixel. """

    # Create a new picture in which each pixel has triple of the 
    # average values of the old pixel triple
    gray_picture = []
    for i in range(len(picture)):
        gray_list = []
        for j in range(len(picture[i])):

            # The average of intensity of the RGB values
            # can be found by adding all the values in the 
            # triples and divide by three
            gray_pixel = (picture[i][j][0] 
                          + picture[i][j][1] 
                          + picture[i][j][2]) // 3

            # The gray pixels are tuples of triple
            # the average values
            gray_list.append((gray_pixel, 
                              gray_pixel, 
                              gray_pixel))
        gray_picture.append(gray_list)
    return gray_picture

def draw_image(yertle, picture):
    """ With a turtle face east, for every pixel on the image, 
        draw a dot that the upper left corner of the drawn image 
        is where the turtle started. """

    # For each row of pixels, draw a dot and move forward. 
    for y in range(len(picture)):
        for x in range(len(picture[y])):
            yertle.dot(1, picture[y][x])
            yertle.forward(1)

        # After each row is finished, move back and get down to 
        # another row.
        yertle.backward(len(picture[0]))
        yertle.right(90)
        yertle.forward(1)
        yertle.left(90)

def ppm_data_to_image(lines):
    """ Make a list of colors (triples) for every pixel 
        in pictures by grouping every three 
        numbers from Lines. """
    
    # Get the dimension of the picture
    space = int(lines[2].find(" "))
    width = int(lines[2][:space])
    length = int(lines[2][space + 1:])

    # Start creating triples from line 5 in Lines
    lines = lines[4:]

    # Create a nested lists of pixel triples using the given
    # dimension from line 2 in Lines.
    image = []
    for _ in range(length):
        triples_list = []
        for _ in range(width):

            # Check if lines is still able to create triples
            if len(lines) >= 3:
                triples = (int(lines[0]), int(lines[1]), 
                           int(lines[2]))
                triples_list.append(triples)

            # Slicing off the last triple in lines to make it 
            # easier to append later triples
            lines = lines[3:]
        image.append(triples_list)
    return image

def read_file_lines(filename):
    """ Opens and reads a file.  Returns a list of lines 
        from the file. """

    # Make sure we can open the file for reading
    file = open(filename)
    assert file

    # Get all the lines and remove the trailing newlines
    lines = file.readlines()
    file.close()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    return lines

def main(): 
    """ This is the main function. """

    # Load the picture data from the file given on the command line.
    if len(sys.argv) != 2:
        print("usage: python3 draw_picture.py FILENAME")
        sys.exit(1)
    filename = sys.argv[1]
    picture = ppm_data_to_image(read_file_lines(filename))

    # Create the turtle/window, and turn off tracing
    yertle = turtle.Turtle()
    turtle.tracer(False)

    # Move turtle to upper left corner
    yertle.up()
    yertle.goto(-390, 340)  # coordinates are a little weird

    # Apply one or more manipulations, if desired:
    # picture = negative(picture)
    # picture = grayscale(picture)
    # for _ in range(60):  # really blurry!
    #    picture = blur(picture)

    # Draw it!
    draw_image(yertle, picture)
    turtle.mainloop()
    
if __name__ == "__main__":
    main()
