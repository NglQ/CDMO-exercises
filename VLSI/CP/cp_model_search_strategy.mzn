include "globals.mzn";

% Input
int: width;
int: n;
% Array of circuits (pairs): circuits[i, j] selects the j-th dimension of the
% i-th circuit (dimension 0 is the width, dimension 1 is the height).
array[1..n, 0..1] of int: circuits
array[1..n] of int: areas = [circuits[i, 0] * circuits[i, 1]| i in 1..n];

/*
Minimum height is given by the max between the highest given circuit and the
the minimal bounding box height (total area divided by width).
Maximum height is given by a first fit approximation.
*/
int: max_height;
int: min_height = max([sum(areas) div width, max(col(circuits, 1))]);

var min_height..max_height: height;
array[1..n] of var 0..(width - min(col(circuits, 0))): positions_x;
array[1..n] of var 0..(max_height - min(col(circuits, 1))): positions_y;

% Constrain overlapping rectangles
constraint diffn(
  positions_x,
  positions_y,
  col(circuits, 0),
  col(circuits, 1));

% Constrain domain
constraint max([positions_x[i] + circuits[i, 0]| i in 1..n]) <= width;
constraint height = max([positions_y[i] + circuits[i, 1]| i in 1..n]);

% Redundant constraints
% The task implicitly solves a scheduling task with limited resources
% on both axes.
constraint redundant_constraint(cumulative(
  positions_x, col(circuits, 0), col(circuits, 1), height));
constraint redundant_constraint(cumulative(
  positions_y, col(circuits, 1), col(circuits, 0), width));

% Symmetry breaking constraints
/*
Horizontal symmetry is given by solutions where all the elements are "flipped"
so that circuit_new_x = width - circuit_x - circuit_width.
By imposing lexicographic ordering we avoid the existence of such a solution.
*/
constraint symmetry_breaking_constraint(lex_lesseq(
  positions_x,
  [width - positions_x[i] - circuits[i, 0]| i in 1..n]));

% Vertical symmetry can be broken similarly.
constraint symmetry_breaking_constraint(lex_lesseq(
  positions_y,
  [height - positions_y[i] - circuits[i, 1]| i in 1..n]));

% Break symmetry with identical chips
% However, these instances (without rotation) do not present identical chips
constraint symmetry_breaking_constraint(
  forall (i in 1..n, j in 1..n where i < j) (
   if circuits[i, 0] == circuits[j, 0] /\ circuits[i, 1] == circuits[j, 1] then
      lex_lesseq([positions_x[i], positions_y[i]],
                 [positions_x[j], positions_y[j]])
    endif
  )
);

% Search strategy
/*
Variables (position coordinates) are selected following decreasing area order.
Intuitively, bigger elements shall be placed first. Moreover, such ordering
takes into account the rectangularity of each plate (areas are weighted by the
complementary rectangularity index). Apparently, square-like objects are more
critical than elongated ones.
*/
array[1..n] of float: weighted_areas = [
  areas[i]
  | i in 1..n
];

/*
array[1..n] of float: weighted_areas = [
  (1 - abs(circuits[i, 0] - circuits[i, 1]) / (circuits[i, 0] + circuits[i, 1]))
  * areas[i]
  | i in 1..n
];
*/

array[0..1, 1..n] of var dom_array(positions_x) union dom_array(positions_y): sorted_positions_r =
                    array2d(0..1, 1..n, reverse(sort_by(positions_x, weighted_areas))
                            ++ reverse(sort_by(positions_y, weighted_areas)) );

solve
  :: seq_search([
    int_search([height], input_order, indomain_min),
    int_search([sorted_positions_r[j, i]| j in 0..1, i in 1..n], input_order,
               indomain_min)])
  minimize height;

output [
  "\(width) \(height)\n\(n)\n",
] ++ [
  "\(circuits[i, 0]) \(circuits[i, 1]) \(positions_x[i]) \(positions_y[i])\n"
  | i in 1..n
];
