include "globals.mzn";

% Input
% Array of circuits (pairs): circuits[i, j] selects the j-th dimension of the
% i-th circuit (dimension 0 is the width, dimension 1 is the height).

/*
Minimum height is given by the max between the highest given circuit and the
the minimal bounding box height (total area divided by width).
Maximum height is given by a first fit approximation.
*/

% Constrain overlapping rectangles

% Constrain domain

% Redundant constraints
% The task implicitly solves a scheduling task with limited resources
% on both axes.

% Symmetry breaking constraints
/*
Horizontal symmetry is given by solutions where all the elements are "flipped"
so that circuit_new_x = width - circuit_x - circuit_width.
By imposing lexicographic ordering we avoid the existence of such a solution.
*/

% Vertical symmetry can be broken similarly.

% Break symmetry with identical chips
% However, these instances (without rotation) do not present identical chips

% Search strategy
/*
Variables (position coordinates) are selected following decreasing area order.
Intuitively, bigger elements shall be placed first. Moreover, such ordering
takes into account the rectangularity of each plate (areas are weighted by the
complementary rectangularity index). Apparently, square-like objects are more
critical than elongated ones.
*/
