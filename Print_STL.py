import numpy
from stl import mesh
import stl
import os

def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz

def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)

def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies

def run(letters):
    stl_folder = os.listdir('STLfiles')
    image_extension = '.stl'
    
    if len(letters) == 0: 
        print('Word must have at least 1 letter!')
        raise Exception
    elif len(letters) == 1:
        stl_path = os.path.join('STLfiles/',letters[0]+image_extension)
        stl_file = mesh.Mesh.from_file(stl_path)
        stl_file.save('CombinedSTL/combined.stl', mode=stl.Mode.ASCII)
    else:
        stl_path = os.path.join('STLfiles/',letters[0]+image_extension)
        combined = mesh.Mesh.from_file(stl_path)
        letters.pop(0)
        
        for letter in letters:
            stl_path = os.path.join('STLfiles/',letter+image_extension)
            stl_file = mesh.Mesh.from_file(stl_path)
            
            _, _, miny, maxy, _, _ = find_mins_maxs(combined)
            l1 = maxy - miny
            
            translate(stl_file, l1, l1 / 10., 1, 'y')
            combined = mesh.Mesh(numpy.concatenate([combined.data] + [stl_file.data]))
        
        combined.save('CombinedSTL/combined_letters.stl', mode=stl.Mode.ASCII)  # save as ASCII
    