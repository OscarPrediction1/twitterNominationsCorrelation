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
	<tr>
		<td>results.csv</td>
		<td>Erster Versuch. Filme in ihrer original Groß/Kleinschreibung abgefragt</td>
	</tr>
	<tr>
		<td>results2.csv</td>
		<td>Text-Corpus auf Lowercase formattiert und alle Queries auch in Lowercase. Zeichenkette "The" durch "" ersetzt</td>
	</tr>
</table>