"""
field unit test file
"""

from ESMF import *
from ESMF.interface.cbindings import *
from ESMF.test.base import TestBase, attr
from ESMF.test.test_api.mesh_utilities import mesh_create_50, mesh_create_50_parallel


class TestField(TestBase):
    def examine_field_attributes(self, field):
        # ~~~~~~~~~~~~~~~~~~~~~~  STAGGER LOCATION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        assert (type(field.staggerloc) is int)

        # ~~~~~~~~~~~~~~~~~~~~~~  BOUNDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        assert (type(field.lower_bounds is np.ndarray))
        assert (field.lower_bounds.shape == tuple([field.rank]))
        assert (type(field.upper_bounds is np.ndarray))
        assert (field.upper_bounds.shape == tuple([field.rank]))
        if field.ndbounds:
            assert (type(field.ndbounds) is list)
            assert (len(field.ndbounds) == field.xd)

        # ~~~~~~~~~~~~~~~~~~~~~~  MASK, DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        assert (type(field.mask) is np.ndarray)
        assert (type(field.data) is np.ndarray)
        assert (field.mask.shape == field.data.shape)

    def make_maskedfield(self, array):
        '''
        :param self: TestMaskedArray class type
        :param array: maxindices of a 2- or 3d array
        :type array: np.array of dtype=np.int32
        '''

        grid = Grid(array, coord_sys=CoordSys.CART)

        mask = grid.add_item(GridItem.MASK)
        mask[:] = 1
        mask[0,1] = 0

        field = Field(grid, "name", ndbounds=[2,5], mask_values=[0])

        assert(np.all(field.mask[:,:,0,1] == True))

        return field

    def test_meta_del(self):
        self.maskedfield = self.make_maskedfield(np.array([10, 10], dtype=np.int32))
        self.maskedfield.meta["test"] = "testmetaobject"
        assert (self.maskedfield.meta["test"] ==  "testmetaobject")
        del (self.maskedfield)
        assert (not hasattr(self, 'maskedfield'))

    @attr('serial')
    @attr('slow')
    #nosetests src/ESMF/test/test_api/test_field.py:TestField.test_field_create_2d_grid
    def test_field_create_2d_grid(self):
        # NOTE: most are commented out to prevent average nose users from using up all available machine memory
        keywords = dict(
            # periodic specifies all valid combos of [num_peri_dims, periodic_dim, pole_dim]
            # periodic=[[None, None, None], [None, None, 0], [None, None, 1],
            #           [0, None, None], [0, None, 0], [0, None, 1],
            #           [1, None, None], [1, 0, 1], [1, 1, 0]],
            # staggerloc=[None, StaggerLoc.CENTER, StaggerLoc.EDGE1, StaggerLoc.EDGE2, StaggerLoc.CORNER],
            # coord_sys=[None, CoordSys.CART, CoordSys.SPH_DEG, CoordSys.SPH_RAD],
            typekind_grid=[None, TypeKind.I4, TypeKind.I8, TypeKind.R4, TypeKind.R8],
            # mask_values = [None, [2], [2, 3, 4]],
            typekind_field=[None, TypeKind.I4, TypeKind.I8, TypeKind.R4, TypeKind.R8],
            # ndbounds=[None, [2], [2, 5]]
            )

        testcases = self.iter_product_keywords(keywords)
        fail = 0
        for a in testcases:
            try:
                grid = Grid(np.array([12, 12]),
                            num_peri_dims=a.periodic[0], periodic_dim=a.periodic[1], pole_dim=a.periodic[2],
                            coord_sys=a.coord_sys, coord_typekind=a.typekind_grid, staggerloc=a.staggerloc)
                if a.mask_values is not None and a.staggerloc is not None:
                    grid.add_item(GridItem.MASK, staggerloc=a.staggerloc)
                    for b in a.mask_values:
                        grid.mask[a.staggerloc][:, b] = b

                field = Field(grid, "test_field_grid_2d", typekind=a.typekind_field, staggerloc=a.staggerloc,
                              ndbounds=a.ndbounds, mask_values=a.mask_values)

                field2 = None
                if a.ndbounds is not None:
                    if len(a.ndbounds) == 1:
                        field2 = field[1, 2:10, 7:9]
                    elif len(a.ndbounds) == 2:
                        field2 = field[1, 2:4, 2:10, 7:9]
                else:
                    field2 = field[2:10, 7:9]
                self.examine_field_attributes(field)
                self.examine_field_attributes(field2)
            except:
                fail += 1
                print a
                break

        if fail > 0:
            raise ValueError(
                "The following combinations of parameters failed to create a proper Field: " + str(fail))

    @attr('serial')
    @attr('slow')
    def test_field_create_3d_grid(self):
        # NOTE: most are commented out to prevent average nose users from using up all available machine memory
        keywords = dict(
            # periodic specifies all valid combos of [num_peri_dims, periodic_dim, pole_dim]
            # periodic=[[None, None, None], [None, None, 0], [None, None, 1], [None, None, 2],
            #           [0, None, None], [0, None, 0], [0, None, 1], [0, None, 2],
            #           [1, None, None], [1, 0, 1], [1, 0, 2], [1, 1, 0], [1, 1, 2], [1, 2, 0], [1, 2, 1]],
            # staggerloc=[None, StaggerLoc.CENTER_VCENTER, StaggerLoc.EDGE1_VCENTER, StaggerLoc.EDGE2_VCENTER,
            #             StaggerLoc.CORNER_VCENTER, StaggerLoc.CENTER_VFACE, StaggerLoc.EDGE1_VFACE,
            #             StaggerLoc.EDGE2_VFACE, StaggerLoc.CORNER_VFACE],
            # coord_sys=[None, CoordSys.CART, CoordSys.SPH_DEG, CoordSys.SPH_RAD],
            # mask_values=[None, [2], [2, 3, 4]],
            typekind_grid=[None, TypeKind.I4, TypeKind.I8, TypeKind.R4, TypeKind.R8],
            typekind_field=[None, TypeKind.I4, TypeKind.I8, TypeKind.R4, TypeKind.R8],
            # ndbounds=[None, [2], [2, 5]]
            )

        testcases = self.iter_product_keywords(keywords)
        fail = []
        for a in testcases:
            try:
                grid = Grid(np.array([12, 12, 12]),
                            num_peri_dims=a.periodic[0], periodic_dim=a.periodic[1], pole_dim=a.periodic[2],
                            coord_sys=a.coord_sys, coord_typekind=a.typekind_grid, staggerloc=a.staggerloc)
                if a.mask_values is not None and a.staggerloc is not None:
                    grid.add_item(GridItem.MASK, staggerloc=a.staggerloc)
                    for b in a.mask_values:
                        grid.mask[a.staggerloc][:, :, b] = b

                field = Field(grid, "test_field_grid_2d", typekind=a.typekind_field, staggerloc=a.staggerloc,
                              ndbounds=a.ndbounds, mask_values=a.mask_values)
                self.examine_field_attributes(field)
                field2 = None
                if a.ndbounds is not None:
                    if len(a.ndbounds) == 1:
                        field2 = field[1, 2:10, 7:9, 4:11]
                    elif len(a.ndbounds) == 2:
                        field2 = field[1, 2:4, 2:10, 7:9, 4:11]
                else:
                    field2 = field[2:10, 7:9, 4:11]
                self.examine_field_attributes(field2)

            except:
                fail += a

        if len(fail) > 0:
            raise ValueError(
                "The following combinations of parameters failed to create a proper Field: " + str(len(fail)))

    @attr('serial')
    @attr('slow')
    def test_field_create_2d_mesh(self):
        parallel = False
        if pet_count() > 1:
            if pet_count() > 4:
                raise NameError('MPI rank must be 4 in parallel mode!')
            parallel = True

        keywords = dict(
            meshloc=[MeshLoc.NODE, MeshLoc.ELEMENT],
            typekind_field=[None, TypeKind.I4, TypeKind.I8, TypeKind.R4, TypeKind.R8],
        )
        # TODO: Mesh masking, periodicity?
        # TODO: extra dimensions on a mesh?

        testcases = self.iter_product_keywords(keywords)
        fail = []
        for a in testcases:
            try:
                # create mesh
                mesh = None
                if parallel:
                    mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                        mesh_create_50_parallel()
                else:
                    mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                        mesh_create_50()

                field = Field(mesh, "test_field_mesh_2d", typekind=a.typekind_field, meshloc=a.meshloc)
                self.examine_field_attributes(field)
                field2 = field[2:10]
                self.examine_field_attributes(field2)

            except:
                fail += a

        if len(fail) > 0:
            raise ValueError(
                "The following combinations of parameters failed to create a proper Field: " + str(len(fail)))

    # TODO: 3d Field mesh?

    def test_field_mask(self):

        max_index = np.array([12, 20])

        grid = Grid(max_index)

        # Add coordinates
        grid.add_coords(staggerloc=[StaggerLoc.CENTER])

        # Add Mask
        mask = grid.add_item(GridItem.MASK)

        [x, y] = [0, 1]
        for i in xrange(mask.shape[x]):
            for j in xrange(mask.shape[y]):
                if (i == 2.0):
                    mask[i, j] = 2
                elif (i == 3.0):
                    mask[i, j] = 3
                else:
                    mask[i, j] = 0

        # create a Field on the Grid, should inherit the mask
        field = Field(grid, "FIELD!", mask_values=[2, 3])
        self.examine_field_attributes(field)

        if pet_count() == 0:
            assert (all(field.mask[2, :]))
            assert (all(field.mask[3, :]))

    def test_field_mask_with_xd(self):

        grid = Grid(np.array([10, 10], dtype=np.int32), coord_sys=CoordSys.CART)

        mask = grid.add_item(GridItem.MASK)
        mask[:] = 1
        mask[0, 1] = 0

        field = Field(grid, "name", ndbounds=[2, 5], mask_values=[0])
        self.examine_field_attributes(field)

        assert (np.all(field.mask[:, :, 0, 1]))

    def test_field_mask_3D(self):

        max_index = np.array([10, 20, 30])

        grid = Grid(max_index)

        # Add coordinates
        grid.add_coords(staggerloc=[StaggerLoc.CENTER])

        # Add Mask
        mask = grid.add_item(GridItem.MASK)

        [x, y, z] = [0, 1, 2]
        for i in xrange(mask.shape[x]):
            for j in xrange(mask.shape[y]):
                for k in xrange(mask.shape[z]):
                    if (i == 1.0):
                        mask[i, j, k] = 2
                    elif (j == 2.0):
                        mask[i, j, k] = 3
                    else:
                        mask[i, j, k] = 0

        # create a Field on the Grid, should inherit the mask
        field = Field(grid, "FIELD!", mask_values=[2, 3])
        self.examine_field_attributes(field)

        assert (np.all(field.mask[1, :, :]))
        assert (np.all(field.mask[:, 2, :]))

    def test_field_mask_3D_with_xd(self):

        grid = Grid(np.array([10, 10, 10], dtype=np.int32), coord_sys=CoordSys.CART)

        mask = grid.add_item(GridItem.MASK)
        mask[...] = 1
        mask[0, 1, 0] = 0

        field = Field(grid, "name", ndbounds=[2, 5], mask_values=[0])
        self.examine_field_attributes(field)

        assert (np.all(field.mask[:, :, 0, 1, 0]))

    def test_field_uniqueness(self):
        # create mesh
        parallel = False
        if pet_count() > 1:
            if pet_count() > 4:
                raise NameError('MPI rank must be 4 in parallel mode!')
            parallel = True

        mesh = None
        if parallel:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50_parallel()
        else:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50()

        field = Field(mesh, 'Field!',
                         TypeKind.I4,
                         MeshLoc.NODE)
        self.examine_field_attributes(field)

        field2 = Field(mesh, 'Field!',
                          typekind=TypeKind.I4,
                          meshloc=MeshLoc.ELEMENT)
        self.examine_field_attributes(field2)

        for i in range(field.shape[0]):
            field.data[i] = 10

        for i in range(field2.shape[0]):
            field2.data[i] = 10

        assert (field.struct.ptr != field2.struct.ptr)

    def test_field_switchedindices_grid(self):
        # create grid
        max_index = np.array([12, 20])
        grid = Grid(max_index, num_peri_dims=1,
                    coord_sys=CoordSys.SPH_RAD,
                    staggerloc=[StaggerLoc.CENTER])

        gridtofieldmap = np.array([2, 1])

        field = Field(grid, 'Field!', TypeKind.R8,
                         ndbounds=gridtofieldmap)

        field2 = Field(grid, 'Field!',
                          ndbounds=np.array([2, 1]))

        field.data[...] = 10
        self.examine_field_attributes(field)

        field2.data[...] = 10
        self.examine_field_attributes(field2)


    def test_field_extradims_grid(self):
        max_index = np.array([12, 20])
        grid = Grid(max_index, num_peri_dims=1,
                    coord_sys=CoordSys.SPH_RAD,
                    staggerloc=[StaggerLoc.CENTER])

        gridtofieldmap = np.array([2, 5])
        field = Field(grid, 'Field!', TypeKind.R8,
                      ndbounds=gridtofieldmap)

        field2 = Field(grid, 'Field!',
                      ndbounds=np.array([2, 5]))

        field.data[...] = 10
        self.examine_field_attributes(field)

        field2.data[...] = 10
        self.examine_field_attributes(field2)


    def test_field_extradims_mesh(self):
        # create mesh
        parallel = False
        if pet_count() > 1:
            if pet_count() > 4:
                raise NameError('MPI rank must be 4 in parallel mode!')
            parallel = True

        mesh = None
        if parallel:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50_parallel()
        else:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50()

        field = Field(mesh, 'Field!',
                         TypeKind.R8,
                         MeshLoc.NODE)
        field2 = Field(mesh, 'Field!',
                          meshloc=MeshLoc.ELEMENT,
                          ndbounds=np.array([2, 5]))

        field.data[...] = 10
        self.examine_field_attributes(field)

        field2.data[...] = 10
        self.examine_field_attributes(field2)

    @attr('serial')
    def test_field_slice_grid(self):
        typekind = TypeKind.R8
        grid = Grid(np.array([100, 100]), coord_sys=CoordSys.CART,
                    coord_typekind=typekind, staggerloc=[StaggerLoc.CENTER])

        grid_row = grid.get_coords(0, staggerloc=StaggerLoc.CENTER)
        grid_col = grid.get_coords(1, staggerloc=StaggerLoc.CENTER)

        row = np.random.rand(100, 100)
        col = np.random.rand(100, 100)

        grid_row[:] = row
        grid_col[:] = col

        grid.add_item(GridItem.MASK)
        grid.add_item(GridItem.AREA)

        field = Field(grid, "GRIDFIELD!", staggerloc=StaggerLoc.CENTER)
        self.examine_field_attributes(field)

        field2 = field[0:5, 0:5]
        self.examine_field_attributes(field2)

        field3 = field2[2:4, 2:4]
        self.examine_field_attributes(field3)

        assert (field.shape == (100, 100))
        assert (field2.shape == (5, 5))
        assert (field3.shape == (2, 2))

        assert (field.upper_bounds.tolist() == [100, 100])
        assert (field2.upper_bounds.tolist() == [5, 5])
        assert (field3.upper_bounds.tolist() == [2, 2])

        assert (field.grid.upper_bounds.tolist() == [100, 100])
        assert (field2.grid.upper_bounds.tolist() == [5, 5])
        assert (field3.grid.upper_bounds.tolist() == [2, 2])

    @attr('serial')
    def test_field_slice_mesh(self):
        # create mesh
        parallel = False
        if pet_count() > 1:
            if pet_count() > 4:
                raise NameError('MPI rank must be 4 in parallel mode!')
            parallel = True

        mesh = None
        if parallel:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50_parallel()
        else:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50()

        field = Field(mesh, 'Field!',
                      TypeKind.R8,
                      MeshLoc.NODE)
        self.examine_field_attributes(field)

        field2 = field[0:5]
        self.examine_field_attributes(field2)

        field3 = field2[2:4]
        self.examine_field_attributes(field3)

        assert (field.shape == (64,))
        assert (field2.shape == (5,))
        assert (field3.shape == (2,))

        assert (field.upper_bounds.tolist() == [64])
        assert (field2.upper_bounds.tolist() == [5])
        assert (field3.upper_bounds.tolist() == [2])

        assert (field.grid.size == 64)
        assert (field2.grid.size == 5)
        assert (field3.grid.size == 2)

    @attr('serial')
    def test_field_slice_grid_extraindices(self):
        n = 10
        grid = Grid(np.array([n,n]), coord_sys=CoordSys.CART, staggerloc=StaggerLoc.CENTER)

        grid_row = grid.get_coords(0, staggerloc=StaggerLoc.CENTER)
        grid_col = grid.get_coords(1, staggerloc=StaggerLoc.CENTER)

        row = np.arange(0, n, 1)

        grid_row[...] = row.reshape((row.size,1))
        grid_col[...] = row.reshape((1,row.size))

        field = Field(grid, "GRIDFIELD!", ndbounds=[2, 5])
        self.examine_field_attributes(field)

        for i in range(2):
            for j in range(5):
                field[i,j,...] = i+j

        field2 = field[0:1, 0:2, 0:5, 0:5]
        self.examine_field_attributes(field2)

        field3 = field2[0:1, 0:1, 2:4, 2:4]
        self.examine_field_attributes(field3)

        assert field.shape == (2, 5, 10, 10)
        assert field2.shape == (1, 2, 5, 5)
        assert field3.shape == (1, 1, 2, 2)

        assert (field.upper_bounds.tolist() == [2, 5, 10, 10])
        assert (field2.upper_bounds.tolist() == [1, 2, 5, 5])
        assert (field3.upper_bounds.tolist() == [1, 1, 2, 2])

        assert (field.grid.upper_bounds.tolist() == [10, 10])
        assert (field2.grid.upper_bounds.tolist() == [5, 5])
        assert (field3.grid.upper_bounds.tolist() == [2, 2])

    @attr('serial')
    def disable_est_field_slice_mesh_extraindices(self):
        # create mesh
        parallel = False
        if pet_count() > 1:
            if pet_count() > 4:
                raise NameError('MPI rank must be 4 in parallel mode!')
            parallel = True

        mesh = None
        if parallel:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50_parallel()
        else:
            mesh, nodeCoord, nodeOwner, elemType, elemConn = \
                mesh_create_50()

        field = Field(mesh, 'Field!',
                      TypeKind.R8,
                      MeshLoc.NODE, ndbounds=[2, 5])
        self.examine_field_attributes(field)

        for i in range(2):
            for j in range(5):
                field[i, j, ...] = i + j

        field2 = field[0:1, 0:2, 0:5]
        self.examine_field_attributes(field2)

        field3 = field2[0:1, 1:2, 2:4]
        self.examine_field_attributes(field3)

        assert field.shape == (2, 5, 10)
        assert field2.shape == (1, 2, 5)
        assert field3.shape == (1, 1, 2)
