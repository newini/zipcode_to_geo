# create temp folder
$temp = 'temp'
New-Item -Path ${temp} -ItemType Directory -Force

# download latidue longitude csv data
# and unzip
For ($i=1; $i -lt 48; $i++) {
    $zip_file = '{0:d2}000-17.0b.zip' -f $i
    echo "Process for ${zip_file}"
    # download
    wget "https://nlftp.mlit.go.jp/isj/dls/data/17.0b/${zip_file}" -OutFile ${temp}\${zip_file}

    # unzip
    Expand-Archive ${temp}\${zip_file} -DestinationPath ${temp}\.

    # move item
    $folder = '{0:d2}000-17.0b' -f $i
    $csv_file = '{0:d2}_2023.csv' -f $i
    mv ${temp}\${folder}\${csv_file} ${temp}\. -Force

    # remove header
    if ($i -ne 1) {
        (Get-Content ${temp}\${csv_file} | Select-Object -Skip 1) | Set-Content ${temp}\${csv_file}
    }

    # clean
    rm ${temp}\${zip_file}
    rm ${temp}\${folder} -r -Force
}

# merge csv files
$new_csv_file = 'latitude_longitude.csv'
echo "Create ${new_csv_file}"
Get-Content ${temp}\*.csv | Set-Content data\${new_csv_file}
                                            

# clean 
rm ${temp} -r -Force