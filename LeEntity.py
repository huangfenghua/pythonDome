from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date
BaseModel = declarative_base()
class Video(BaseModel):
    __tablename__ = 't_video_le'
    id = Column(Integer, primary_key=True)
    cate_id = Column(Integer, nullable=True)
    y_vid = Column(Integer, nullable=True)
    super_id = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    title = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    describe = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    director_names = Column(String, nullable=True)
    actor_names = Column(String, nullable=True)
    type_names = Column(String, nullable=True)
    area_names = Column(String, nullable=True)
    language = Column(String, nullable=True)
    release_year_names = Column(String, nullable=True)
    release_year_id = Column(Integer, nullable=True)
    update_time = Column(String, nullable=True)
    create_time = Column(String, nullable=True)
    introduce = Column(String, nullable=True)
    video_url = Column(String, nullable=True, default='')
    download_url = Column(String, nullable=True, default='')
    w_name = Column(String, nullable=True, default='')
    duration = Column(String, nullable=True, default='')
    today_play_times = Column(Integer, nullable=True)
    total_score = Column(Integer, nullable=True)
    score_count = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True, default=0)
    is_del = Column(Integer, nullable=True, default=0)
    update_video_time = Column(Date, nullable=True)
    update_video_mill = Column(Integer, nullable=True, default=0)



class VideoSubset(BaseModel):
    __tablename__ = 't_video_subset_le'
    id = Column(Integer, primary_key=True)
    v_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    download_url = Column(String, nullable=True)
    sort = Column(Integer, nullable=True)
    update_time = Column(String, nullable=True)
    update_video_time = Column(String, nullable=True)
    update_video_mill = Column(String, nullable=True)
