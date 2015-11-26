# twitterNominationsCorrelation
Try to make sense of historic twitter data provided by MIT in correlation with the past oscar nominees

## Installation

1) Just run 

```bash
pip install -r requirements.txt
```

in projects home directory.

2) Rename `example.db.py` to `db.py` and enter your MongoDB connection string to the file.

## Results

<table>
	<thead>
		<tr>
			<th>Filename</th>
			<th>Description</th>
			<th>Logistic regression p-value</th>
		</tr>
	</thead>
	<tr>
		<td>results.csv</td>
		<td>Firsty try. Movies in their original uppercase/lowercase names.</td>
		<td>0.4</td>
	</tr>
	<tr>
		<td>results2.csv</td>
		<td>Text-corpus to lowercase and also queries to lowercase to unify them. Replaced string "The" with ""</td>
		<td>0.6421</td>
	</tr>
</table>