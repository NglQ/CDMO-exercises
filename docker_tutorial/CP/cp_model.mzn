include "globals.mzn";

int: width;
int: n;

array[1..n, 0..1] of int: circuits;
array[1..n] of int: areas = [circuits[i, 0] * circuits[i, 1]| i in 1..n];

int: max_height;
int: min_height = max([sum(areas) div width, max(col(circuits, 1))]);

var min_height..max_height: height;
array[1..n] of var 0..(width - min(col(circuits, 0))): positions_x;
array[1..n] of var 0..(max_height - min(col(circuits, 1))): positions_y;

constraint diffn(
  positions_x,
  positions_y,
  col(circuits, 0),
  col(circuits, 1));

constraint max([positions_x[i] + circuits[i, 0]| i in 1..n]) <= width;
constraint height = max([positions_y[i] + circuits[i, 1]| i in 1..n]);


constraint redundant_constraint(cumulative(
  positions_x, col(circuits, 0), col(circuits, 1), height));
constraint redundant_constraint(cumulative(
  positions_y, col(circuits, 1), col(circuits, 0), width));


constraint symmetry_breaking_constraint(lex_lesseq(
  positions_x,
  [width - positions_x[i] - circuits[i, 0]| i in 1..n]));

constraint symmetry_breaking_constraint(lex_lesseq(
  positions_y,
  [height - positions_y[i] - circuits[i, 1]| i in 1..n]));


constraint symmetry_breaking_constraint(
  forall (i in 1..n, j in 1..n where i < j) (
   if circuits[i, 0] == circuits[j, 0] /\ circuits[i, 1] == circuits[j, 1] then
      lex_lesseq([positions_x[i], positions_y[i]],
                 [positions_x[j], positions_y[j]])
    endif
  )
);

array[1..n] of float: weighted_areas = [
  areas[i]
  | i in 1..n
];

array[0..1, 1..n] of var dom_array(positions_x) union dom_array(positions_y): sorted_positions_r =
                    array2d(0..1, 1..n, reverse(sort_by(positions_x, weighted_areas))
                            ++ reverse(sort_by(positions_y, weighted_areas)) );

solve
  :: seq_search([
    int_search([height], input_order, indomain_min),
    int_search([sorted_positions_r[j, i]| j in 0..1, i in 1..n], input_order,
               indomain_min)])
  minimize height;

/*output [
  "\(width) \(height)\n\(n)\n",
] ++ [
  "\(circuits[i, 0]) \(circuits[i, 1]) \(positions_x[i]) \(positions_y[i])\n"
  | i in 1..n
];*/
