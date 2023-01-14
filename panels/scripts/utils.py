import pandas as pd
import contextlib
import sqlite3
import numpy as np

datasets = ["/data/elferich/cisTEM_projects/ER_Hox_120h_20211029_g1_l1/ER_Hox_120h_20211029_g1_l1_thickness_nodes.db",
            ]

dataset_names = ["euc_lamella1",
                 ]

dataset_info = [(dataset,dataset_names[i]) for i,dataset in enumerate(datasets)]
                 

def get_tm_data_from_db(dataset):
    # Open the database
    with contextlib.closing(sqlite3.connect(dataset)) as con:
        df1 = pd.read_sql_query("SELECT * FROM TEMPLATE_MATCH_LIST", con)
    return df1

def get_thickness_data_from_db(dataset, ctf_job_id):
    # Open the database
    with contextlib.closing(sqlite3.connect(dataset)) as con:
        df1 = pd.read_sql_query(f"SELECT CTF.SAMPLE_THICKNESS as SAMPLE_THICKNESS, MOVIE_ASSETS.FILENAME as movie_filename FROM IMAGE_ASSETS LEFT JOIN (SELECT CTF_ESTIMATION_ID, SAMPLE_THICKNESS, IMAGE_ASSET_ID FROM ESTIMATED_CTF_PARAMETERS WHERE ESTIMATED_CTF_PARAMETERS.CTF_ESTIMATION_JOB_ID = {ctf_job_id}) AS CTF  ON CTF.IMAGE_ASSET_ID = IMAGE_ASSETS.IMAGE_ASSET_ID INNER JOIN MOVIE_ASSETS ON IMAGE_ASSETS.PARENT_MOVIE_ID = MOVIE_ASSETS.MOVIE_ASSET_ID  ", con)
    return df1

def get_data_from_db(dataset,get_movement=False):
    with contextlib.closing(sqlite3.connect(dataset)) as con:

        df1 = pd.read_sql_query(f"SELECT IMAGE_ASSET_ID,MOVIE_ASSET_ID,IMAGE_ASSETS.FILENAME, MOVIE_ASSETS.FILENAME as movie_filename, CTF_ESTIMATION_ID , ALIGNMENT_ID, IMAGE_ASSETS.PIXEL_SIZE as image_pixel_size, MOVIE_ASSETS.PIXEL_SIZE as movie_pixel_size, IMAGE_ASSETS.X_SIZE, IMAGE_ASSETS.Y_SIZE, IMAGE_ASSETS.ORIGINAL_X_SIZE, IMAGE_ASSETS.ORIGINAL_Y_SIZE, IMAGE_ASSETS.CROP_CENTER_X, IMAGE_ASSETS.CROP_CENTER_Y  FROM IMAGE_ASSETS INNER JOIN MOVIE_ASSETS ON MOVIE_ASSETS.MOVIE_ASSET_ID == IMAGE_ASSETS.PARENT_MOVIE_ID", con)
        df2 = pd.read_sql_query("SELECT CTF_ESTIMATION_ID,DEFOCUS1,DEFOCUS2,DEFOCUS_ANGLE,OUTPUT_DIAGNOSTIC_FILE,SCORE, DETECTED_RING_RESOLUTION FROM ESTIMATED_CTF_PARAMETERS",con)
        selected_micrographs = pd.merge(df1,df2,on="CTF_ESTIMATION_ID")
        df3 = pd.read_sql_query(f"SELECT MOVIE_ASSET_ID,IMAGE_SHIFT_X, IMAGE_SHIFT_Y, CONTENT_JSON FROM MOVIE_ASSETS_METADATA",con)
        selected_micrographs = pd.merge(selected_micrographs,df3,on="MOVIE_ASSET_ID")
        selected_micrographs["TOTAL_MOVEMENT"] = 0
        if get_movement:
            prev_shift = None
            for i, row in selected_micrographs.iterrows():
                df4 = pd.read_sql_query(f"SELECT FRAME_NUMBER, X_SHIFT, Y_SHIFT FROM MOVIE_ALIGNMENT_PARAMETERS_{row['ALIGNMENT_ID']}",con)
                total_movement = 0
                for j, mrow in df4.iterrows():
                    if prev_shift is None:
                        prev_shift = np.array([mrow["X_SHIFT"],mrow["Y_SHIFT"]])
                        continue
                    movement = np.linalg.norm(prev_shift-np.array([mrow["X_SHIFT"],mrow["Y_SHIFT"]]))
                    total_movement += movement
                    prev_shift = np.array([mrow["X_SHIFT"],mrow["Y_SHIFT"]])
                selected_micrographs.at[i,'TOTAL_MOVEMENT'] = total_movement
    return(selected_micrographs)