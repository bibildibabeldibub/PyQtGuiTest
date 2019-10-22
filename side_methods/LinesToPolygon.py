import warnings

def lines_to_polygon(lines):

    polygon = lines.pop(0)
    while len(lines) > 0:
        i = 0
        c = lines
        for x in range(len(lines)):
            l = lines[i]
            if l[0] == polygon[0]:
                polygon.insert(0, l[1])
                lines.pop(i)
                i -= 1
            elif l[1] == polygon[0]:
                polygon.insert(0, l[0])
                lines.pop(i)
                i -= 1

            if l[0] == polygon[-1]:
                polygon.append(l[1])
                lines.pop(i)
                i -= 1
            elif l[1] == polygon[-1]:
                polygon.append(l[0])
                lines.pop(i)
                i -= 1
            i += 1

        if c == lines:
            warnings.warn('SomeThing Wrong while transforming lines to polygons')

    return polygon

